# Android — Transport Feature Implementation Guide
**Date:** 2026-11-16  
**Backend URL:** `https://mithran.co.in`  
**Prepared for:** Android Studio / Kotlin developer  

---

## Overview of What to Build

Three additions to the parent-facing app:

| Screen / Feature | Trigger |
|---|---|
| **"My Bus" card** on home screen | Always visible if student has transport allocation |
| **Bus Tracking screen** | Tap the card → full screen with route info, driver contact, live map |
| **Boarding push notification** | Server sends when child is marked as boarded or missed |

---

## 1. API — Get Bus Info

### Endpoint
```
GET https://mithran.co.in/mobi/transport/?username=<username>
Authorization: Bearer <access_token>
```

The `username` and `access_token` are already in the app from login — same pattern as attendance, fees, etc.

### Success Response (student has a bus)
```json
{
  "route": {
    "code": "R01",
    "name": "Coimbatore North Route"
  },
  "stop": {
    "name": "Gandhipuram",
    "area": "Town",
    "pickup_time": "07:30",
    "drop_time": "16:15"
  },
  "vehicle": {
    "name": "School Bus 4",
    "number": "TN33 AB 1234"
  },
  "driver": {
    "name": "Rajan",
    "mobile": "9876543210"
  },
  "live": {
    "lat": 11.0168,
    "lng": 76.9558,
    "speed_kmh": 32.5,
    "heading": 180,
    "timestamp": "2026-11-16T07:42:00Z"
  }
}
```

**Null cases to handle:**
- `live` → `null` : vehicle has no GPS ping yet. Show "Location not available yet."
- `vehicle` → `null` : no vehicle assigned. Hide vehicle row.
- `driver` → `null` : no driver assigned. Hide driver row.
- Entire response `{ "transport": null }` : student not assigned to any bus. Hide the "My Bus" card entirely.

### HTTP errors
- `401` → token expired, refresh and retry (same flow as other APIs)
- `404` → student not found

---

## 2. Kotlin Data Classes

```kotlin
data class TransportResponse(
    val route: RouteInfo?,
    val stop: StopInfo?,
    val vehicle: VehicleInfo?,
    val driver: DriverInfo?,
    val live: LivePosition?,
    val transport: Any?   // null means "no allocation" when the whole object is { "transport": null }
)

data class RouteInfo(
    val code: String,
    val name: String
)

data class StopInfo(
    val name: String,
    val area: String?,
    @SerializedName("pickup_time") val pickupTime: String?,   // "HH:MM" 24-hour
    @SerializedName("drop_time") val dropTime: String?
)

data class VehicleInfo(
    val name: String,
    val number: String
)

data class DriverInfo(
    val name: String,
    val mobile: String
)

data class LivePosition(
    val lat: Double,
    val lng: Double,
    @SerializedName("speed_kmh") val speedKmh: Double,
    val heading: Int,
    val timestamp: String   // ISO-8601 UTC e.g. "2026-11-16T07:42:00Z"
)
```

---

## 3. Retrofit Interface

Add this to your existing API interface (wherever attendance/fees calls are defined):

```kotlin
@GET("mobi/transport/")
suspend fun getTransport(
    @Header("Authorization") token: String,
    @Query("username") username: String
): Response<TransportResponse>
```

Call it exactly like existing endpoints:
```kotlin
val response = apiService.getTransport(
    token = "Bearer $accessToken",
    username = savedUsername
)
```

---

## 4. UI — "My Bus" Card (Home Screen)

Add a card below or alongside the existing Attendance / Fees cards.

**Show this card only if `transport != null` and `route != null`.**

```
┌──────────────────────────────────────────────┐
│  🚌  My Bus                                  │
│  Route: Coimbatore North Route (R01)         │
│  Stop:  Gandhipuram  •  Pickup: 07:30 AM     │
│  Bus:   School Bus 4  •  TN33 AB 1234        │
│                              [ Track Live → ]│
└──────────────────────────────────────────────┘
```

- If `live != null` → show a green dot "● Live" on the card
- If `live == null` → show a grey dot "● No GPS"

---

## 5. UI — Bus Tracking Screen

Open on tap of "Track Live →" button.

### Layout (top to bottom)

```
[ ← Back ]  My Bus

─── Route & Stop ────────────────────────────
  Route:   Coimbatore North Route
  Stop:    Gandhipuram (Town area)
  Pickup:  07:30 AM
  Drop:    04:15 PM

─── Vehicle ──────────────────────────────────
  School Bus 4  •  TN33 AB 1234

─── Driver ───────────────────────────────────
  Rajan
  📞  [9876543210]   ← tappable, opens dialer

─── Live Location ────────────────────────────
  [   Google Map / OSM fragment here   ]
  Bus speed: 32.5 km/h
  Last updated: 07:42 AM  (compute from timestamp)

  [ Refresh ]   ← manual refresh button
```

### Map marker
- Place a **bus icon marker** at `(live.lat, live.lng)`
- Rotate the marker by `live.heading` degrees (0 = North, 90 = East)
- If `live == null` → show map but display a banner: "Live location not available yet. Pull to refresh."

### Auto-refresh
Poll the API every **30 seconds** while the screen is open (use a `Handler` or `LifecycleScope` coroutine with `delay(30_000)`). Stop polling `onPause`, resume `onResume`.

```kotlin
private fun startPolling() {
    viewLifecycleOwner.lifecycleScope.launch {
        while (isActive) {
            fetchTransport()
            delay(30_000)
        }
    }
}
```

### Driver call button
```kotlin
btnCallDriver.setOnClickListener {
    val intent = Intent(Intent.ACTION_DIAL,
        Uri.parse("tel:${driverInfo.mobile}"))
    startActivity(intent)
}
```

---

## 6. Push Notifications — Boarding Alerts

The server sends FCM notifications automatically when staff marks boarding. No change needed to the FCM token registration code — it already works.

### Notification payload sent by server

**Child boarded (morning):**
```
title: "Bus Update"
body:  "Ravi Kumar has boarded Coimbatore North Route at Gandhipuram (07:42 AM)."
```

**Child returned (evening):**
```
title: "Bus Update"
body:  "Ravi Kumar has returned on Coimbatore North Route at Gandhipuram (04:18 PM)."
```

**Child missed bus:**
```
title: "Bus Alert"
body:  "Ravi Kumar has missed the morning bus at Gandhipuram (Coimbatore North Route). Please check."
```

### How to handle in `FirebaseMessagingService`

The notifications arrive as **notification messages** (title + body) — Firebase shows them automatically in the system tray when the app is in background.

If the app is in **foreground**, handle in `onMessageReceived`:

```kotlin
override fun onMessageReceived(remoteMessage: RemoteMessage) {
    val title = remoteMessage.notification?.title ?: return
    val body  = remoteMessage.notification?.body  ?: return

    // Show a local notification in foreground
    showLocalNotification(title, body)
}
```

**Optional deep-link:** To open the Bus Tracking screen when the user taps the notification, add an `Intent` with action `"OPEN_TRANSPORT"` to your notification channel handler. The server can be extended to send a `data` payload alongside `notification` if needed — ask the backend team.

### Notification channel (if not already created)
```kotlin
// In Application.onCreate() or first launch
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
    val channel = NotificationChannel(
        "transport_alerts",
        "Bus Alerts",
        NotificationManager.IMPORTANCE_HIGH
    ).apply {
        description = "Boarding and bus location alerts"
    }
    getSystemService(NotificationManager::class.java)
        .createNotificationChannel(channel)
}
```

---

## 7. Suggested Navigation Flow

```
Home Screen
  └── My Bus card (visible only if allocated)
        └── Tap → BusTrackingFragment / Activity
                    ├── Route, stop, timing info
                    ├── Driver name + call button
                    ├── Live map (auto-refresh 30s)
                    └── Last updated time
```

Suggested placement in the bottom nav or as a section on the home dashboard — same level as Attendance and Fees.

---

## 8. Edge Cases to Handle

| Situation | What to show |
|---|---|
| `transport: null` | Hide "My Bus" card. Don't show transport section. |
| `live: null` | Show route/stop/driver info, map with no marker, "GPS not available" banner |
| `vehicle: null` | Show route and stop, hide vehicle row |
| `driver: null` | Hide driver row and call button |
| `pickup_time: null` | Hide pickup time row |
| Network error | Show cached last-known data with "Could not refresh" toast |
| 401 Unauthorized | Refresh token and retry once, then redirect to login |

---

## 9. Permissions Required (AndroidManifest.xml)

```xml
<!-- For the driver call button -->
<uses-permission android:name="android.permission.CALL_PHONE" />

<!-- For showing the map (if using Google Maps) -->
<!-- Already present if the app uses maps elsewhere -->
```

If using **Google Maps SDK**, add the map fragment as normal. No new API keys needed from the backend — the map only needs the lat/lng coordinates from the API response.

---

## 10. Quick Summary Checklist

- [ ] Add `TransportResponse` data classes
- [ ] Add `getTransport()` to Retrofit interface  
- [ ] Add `TransportViewModel` / repository method
- [ ] Add "My Bus" card to home screen (hide if `transport == null`)
- [ ] Create `BusTrackingFragment` with map, route details, driver call button
- [ ] Auto-poll every 30 s while screen is open
- [ ] Handle `live == null` gracefully (show info, hide marker)
- [ ] Handle boarding push notifications (they arrive automatically, just ensure the notification channel exists)
- [ ] Add `CALL_PHONE` permission for driver call button
