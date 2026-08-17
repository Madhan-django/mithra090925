# Grievance API — Android Implementation Guide

Base URL: `https://mithran.co.in/mobi/`  
Auth: JWT Bearer token (same token used for all other mobi APIs)

---

## Endpoints Summary

| Method | URL | Purpose |
|--------|-----|---------|
| `POST` | `/mobi/grievance/?username=<usernm>` | Submit a new grievance |
| `GET` | `/mobi/grievance/?username=<usernm>` | List all grievances for this student |
| `GET` | `/mobi/grievance/<id>/?username=<usernm>` | Single grievance detail |

---

## Request & Response Shapes

### POST — Submit Grievance

**Request body (JSON):**
```json
{
  "area_of_complaint": "Academic",
  "aoc_other": null,
  "detail": "Teacher is not explaining the lessons clearly.",
  "mobile": "9876543210"
}
```

| Field | Type | Required | Values |
|-------|------|----------|--------|
| `area_of_complaint` | String | Yes | `Academic`, `Non-Academic`, `Activities`, `Transport`, `Office`, `Other` |
| `aoc_other` | String | Only if area = `Other` | Free text |
| `detail` | String | Yes | Max 250 characters |
| `mobile` | String | Yes | Parent contact number |

**Success response — 201:**
```json
{
  "id": 5,
  "area_of_complaint": "Academic",
  "aoc_other": null,
  "detail": "Teacher is not explaining the lessons clearly.",
  "mobile": "9876543210",
  "complaint_date": "2026-08-04T10:30:00Z",
  "complaint_status": "Open",
  "action_date": null,
  "principal_remark": null,
  "concern_person_remark": null,
  "act_details": null,
  "concern_person_name": "Anonymous",
  "no_action_taken": true
}
```

### GET — List / Detail

**Response (list — array of objects, detail — single object):**
```json
{
  "id": 5,
  "area_of_complaint": "Academic",
  "aoc_other": null,
  "detail": "Teacher is not explaining the lessons clearly.",
  "mobile": "9876543210",
  "complaint_date": "2026-08-04T10:30:00Z",
  "complaint_status": "In-progress",
  "action_date": "2026-08-05T09:00:00Z",
  "principal_remark": "Noted, will be addressed.",
  "concern_person_remark": "Meeting with teacher scheduled.",
  "act_details": "Teacher counselled by HOD.",
  "concern_person_name": "Mr. Rajan",
  "no_action_taken": false
}
```

`complaint_status` values: `Open` · `Pending` · `In-progress` · `Resolved`

---

## Step 1 — Data Classes

```kotlin
// model/GrievanceModels.kt

data class GrievanceRequest(
    val area_of_complaint: String,
    val aoc_other: String?,
    val detail: String,
    val mobile: String
)

data class GrievanceResponse(
    val id: Int,
    val area_of_complaint: String,
    val aoc_other: String?,
    val detail: String,
    val mobile: String,
    val complaint_date: String,
    val complaint_status: String,       // Open | Pending | In-progress | Resolved
    val action_date: String?,
    val principal_remark: String?,
    val concern_person_remark: String?,
    val act_details: String?,
    val concern_person_name: String,
    val no_action_taken: Boolean
)
```

---

## Step 2 — Retrofit Interface

Add these three functions to your existing `ApiService` interface (the same one that has `getStudent`, `getHomework`, etc.):

```kotlin
// network/ApiService.kt  (add inside your existing interface)

@GET("grievance/")
suspend fun getGrievances(
    @Header("Authorization") token: String,
    @Query("username") username: String
): List<GrievanceResponse>

@GET("grievance/{id}/")
suspend fun getGrievanceDetail(
    @Header("Authorization") token: String,
    @Query("username") username: String,
    @Path("id") id: Int
): GrievanceResponse

@POST("grievance/")
suspend fun submitGrievance(
    @Header("Authorization") token: String,
    @Query("username") username: String,
    @Body body: GrievanceRequest
): GrievanceResponse
```

---

## Step 3 — Repository

```kotlin
// repository/GrievanceRepository.kt

class GrievanceRepository(private val api: ApiService) {

    suspend fun fetchGrievances(token: String, username: String): Result<List<GrievanceResponse>> {
        return try {
            val list = api.getGrievances("Bearer $token", username)
            Result.success(list)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun submitGrievance(
        token: String,
        username: String,
        request: GrievanceRequest
    ): Result<GrievanceResponse> {
        return try {
            val response = api.submitGrievance("Bearer $token", username, request)
            Result.success(response)
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
```

---

## Step 4 — ViewModel

```kotlin
// viewmodel/GrievanceViewModel.kt

class GrievanceViewModel(private val repo: GrievanceRepository) : ViewModel() {

    private val _grievances = MutableLiveData<List<GrievanceResponse>>()
    val grievances: LiveData<List<GrievanceResponse>> = _grievances

    private val _submitResult = MutableLiveData<Result<GrievanceResponse>>()
    val submitResult: LiveData<Result<GrievanceResponse>> = _submitResult

    val isLoading = MutableLiveData(false)
    val errorMessage = MutableLiveData<String?>()

    fun loadGrievances(token: String, username: String) {
        viewModelScope.launch {
            isLoading.value = true
            val result = repo.fetchGrievances(token, username)
            result.onSuccess { _grievances.value = it }
            result.onFailure { errorMessage.value = it.message }
            isLoading.value = false
        }
    }

    fun submitGrievance(token: String, username: String, request: GrievanceRequest) {
        viewModelScope.launch {
            isLoading.value = true
            val result = repo.submitGrievance(token, username, request)
            _submitResult.value = result
            if (result.isSuccess) loadGrievances(token, username)  // refresh list
            isLoading.value = false
        }
    }
}

// Factory (add alongside ViewModel)
class GrievanceViewModelFactory(private val repo: GrievanceRepository) :
    ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        @Suppress("UNCHECKED_CAST")
        return GrievanceViewModel(repo) as T
    }
}
```

---

## Step 5 — RecyclerView Adapter (list screen)

```kotlin
// adapter/GrievanceAdapter.kt

class GrievanceAdapter(
    private val onItemClick: (GrievanceResponse) -> Unit
) : RecyclerView.Adapter<GrievanceAdapter.VH>() {

    private var items = listOf<GrievanceResponse>()

    fun submitList(list: List<GrievanceResponse>) {
        items = list
        notifyDataSetChanged()
    }

    inner class VH(private val binding: ItemGrievanceBinding) :
        RecyclerView.ViewHolder(binding.root) {

        fun bind(item: GrievanceResponse) {
            binding.tvArea.text = item.area_of_complaint
            binding.tvDetail.text = item.detail
            binding.tvDate.text = item.complaint_date.take(10)  // show date only
            binding.tvStatus.text = item.complaint_status

            // Colour-code the status chip
            val color = when (item.complaint_status) {
                "Open"        -> R.color.status_open        // red
                "Pending"     -> R.color.status_pending     // orange
                "In-progress" -> R.color.status_inprogress  // blue
                "Resolved"    -> R.color.status_resolved    // green
                else          -> R.color.status_open
            }
            binding.tvStatus.setBackgroundColor(
                ContextCompat.getColor(binding.root.context, color)
            )

            binding.root.setOnClickListener { onItemClick(item) }
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int) =
        VH(ItemGrievanceBinding.inflate(LayoutInflater.from(parent.context), parent, false))

    override fun onBindViewHolder(holder: VH, position: Int) = holder.bind(items[position])
    override fun getItemCount() = items.size
}
```

---

## Step 6 — List Fragment

```kotlin
// fragment/GrievanceListFragment.kt

class GrievanceListFragment : Fragment(R.layout.fragment_grievance_list) {

    private var _binding: FragmentGrievanceListBinding? = null
    private val binding get() = _binding!!

    private val viewModel: GrievanceViewModel by viewModels {
        val api = RetrofitClient.instance.create(ApiService::class.java)
        GrievanceViewModelFactory(GrievanceRepository(api))
    }

    private lateinit var adapter: GrievanceAdapter

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        _binding = FragmentGrievanceListBinding.bind(view)

        // Pull token & username from SharedPreferences (same as your other screens)
        val prefs = requireContext().getSharedPreferences("auth", Context.MODE_PRIVATE)
        val token    = prefs.getString("access_token", "") ?: ""
        val username = prefs.getString("username", "") ?: ""

        adapter = GrievanceAdapter { grievance ->
            // Navigate to detail or show a bottom sheet
            val bundle = bundleOf("grievance_id" to grievance.id)
            findNavController().navigate(R.id.action_grievanceList_to_grievanceDetail, bundle)
        }
        binding.recyclerView.adapter = adapter
        binding.recyclerView.layoutManager = LinearLayoutManager(requireContext())

        viewModel.grievances.observe(viewLifecycleOwner) { adapter.submitList(it) }
        viewModel.isLoading.observe(viewLifecycleOwner) {
            binding.progressBar.isVisible = it
        }
        viewModel.errorMessage.observe(viewLifecycleOwner) {
            if (it != null) Toast.makeText(requireContext(), it, Toast.LENGTH_LONG).show()
        }

        binding.fabNewGrievance.setOnClickListener {
            findNavController().navigate(R.id.action_grievanceList_to_grievanceSubmit)
        }

        viewModel.loadGrievances(token, username)
    }

    override fun onDestroyView() { super.onDestroyView(); _binding = null }
}
```

---

## Step 7 — Submit Fragment

```kotlin
// fragment/GrievanceSubmitFragment.kt

class GrievanceSubmitFragment : Fragment(R.layout.fragment_grievance_submit) {

    private var _binding: FragmentGrievanceSubmitBinding? = null
    private val binding get() = _binding!!

    private val viewModel: GrievanceViewModel by viewModels {
        val api = RetrofitClient.instance.create(ApiService::class.java)
        GrievanceViewModelFactory(GrievanceRepository(api))
    }

    // Area choices must match server values exactly
    private val areaChoices = listOf(
        "Academic", "Non-Academic", "Activities", "Transport", "Office", "Other"
    )

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        _binding = FragmentGrievanceSubmitBinding.bind(view)

        val prefs = requireContext().getSharedPreferences("auth", Context.MODE_PRIVATE)
        val token    = prefs.getString("access_token", "") ?: ""
        val username = prefs.getString("username", "") ?: ""

        // Populate area spinner
        val spinnerAdapter = ArrayAdapter(
            requireContext(), android.R.layout.simple_spinner_item, areaChoices
        )
        spinnerAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        binding.spinnerArea.adapter = spinnerAdapter

        // Show/hide "Other" text field
        binding.spinnerArea.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>, v: View?, pos: Int, id: Long) {
                binding.tilAocOther.isVisible = areaChoices[pos] == "Other"
            }
            override fun onNothingSelected(parent: AdapterView<*>) {}
        }

        binding.btnSubmit.setOnClickListener {
            val area     = areaChoices[binding.spinnerArea.selectedItemPosition]
            val aocOther = binding.etAocOther.text.toString().trim().takeIf { it.isNotEmpty() }
            val detail   = binding.etDetail.text.toString().trim()
            val mobile   = binding.etMobile.text.toString().trim()

            // Client-side validation
            if (area == "Other" && aocOther == null) {
                binding.tilAocOther.error = "Please specify"; return@setOnClickListener
            }
            if (detail.isEmpty()) {
                binding.tilDetail.error = "Please describe your complaint"; return@setOnClickListener
            }
            if (detail.length > 250) {
                binding.tilDetail.error = "Max 250 characters"; return@setOnClickListener
            }
            if (mobile.isEmpty()) {
                binding.tilMobile.error = "Mobile number is required"; return@setOnClickListener
            }

            viewModel.submitGrievance(
                token, username,
                GrievanceRequest(
                    area_of_complaint = area,
                    aoc_other = aocOther,
                    detail = detail,
                    mobile = mobile
                )
            )
        }

        viewModel.submitResult.observe(viewLifecycleOwner) { result ->
            result.onSuccess {
                Toast.makeText(requireContext(), "Grievance submitted!", Toast.LENGTH_SHORT).show()
                findNavController().popBackStack()
            }
            result.onFailure {
                Toast.makeText(requireContext(), "Failed: ${it.message}", Toast.LENGTH_LONG).show()
            }
        }

        viewModel.isLoading.observe(viewLifecycleOwner) {
            binding.btnSubmit.isEnabled = !it
            binding.progressBar.isVisible = it
        }
    }

    override fun onDestroyView() { super.onDestroyView(); _binding = null }
}
```

---

## Step 8 — XML Layouts

### `fragment_grievance_list.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <ProgressBar
        android:id="@+id/progressBar"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="center"
        android:visibility="gone" />

    <androidx.recyclerview.widget.RecyclerView
        android:id="@+id/recyclerView"
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        android:padding="8dp"
        android:clipToPadding="false" />

    <com.google.android.material.floatingactionbutton.FloatingActionButton
        android:id="@+id/fabNewGrievance"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_gravity="bottom|end"
        android:layout_margin="16dp"
        android:contentDescription="New Grievance"
        app:srcCompat="@android:drawable/ic_input_add" />

</androidx.coordinatorlayout.widget.CoordinatorLayout>
```

### `item_grievance.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<com.google.android.material.card.MaterialCardView
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:layout_margin="6dp"
    app:cardCornerRadius="8dp"
    app:cardElevation="2dp">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="12dp">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="horizontal">

            <TextView
                android:id="@+id/tvArea"
                android:layout_width="0dp"
                android:layout_height="wrap_content"
                android:layout_weight="1"
                android:textStyle="bold"
                android:textSize="15sp" />

            <TextView
                android:id="@+id/tvStatus"
                android:layout_width="wrap_content"
                android:layout_height="wrap_content"
                android:paddingHorizontal="8dp"
                android:paddingVertical="2dp"
                android:textColor="@android:color/white"
                android:textSize="12sp"
                android:background="@drawable/bg_rounded" />
        </LinearLayout>

        <TextView
            android:id="@+id/tvDetail"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="4dp"
            android:maxLines="2"
            android:ellipsize="end"
            android:textSize="13sp" />

        <TextView
            android:id="@+id/tvDate"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginTop="4dp"
            android:textSize="12sp"
            android:textColor="@android:color/darker_gray" />

    </LinearLayout>

</com.google.android.material.card.MaterialCardView>
```

### `fragment_grievance_submit.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<ScrollView
    xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent">

    <LinearLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:orientation="vertical"
        android:padding="16dp">

        <TextView
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Area of Complaint"
            android:textStyle="bold"
            android:layout_marginBottom="4dp" />

        <Spinner
            android:id="@+id/spinnerArea"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:layout_marginBottom="12dp" />

        <com.google.android.material.textfield.TextInputLayout
            android:id="@+id/tilAocOther"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Specify (if Other)"
            android:visibility="gone"
            android:layout_marginBottom="12dp">

            <com.google.android.material.textfield.TextInputEditText
                android:id="@+id/etAocOther"
                android:layout_width="match_parent"
                android:layout_height="wrap_content" />
        </com.google.android.material.textfield.TextInputLayout>

        <com.google.android.material.textfield.TextInputLayout
            android:id="@+id/tilDetail"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Describe your complaint (max 250 chars)"
            android:layout_marginBottom="12dp"
            app:counterEnabled="true"
            app:counterMaxLength="250"
            xmlns:app="http://schemas.android.com/apk/res-auto">

            <com.google.android.material.textfield.TextInputEditText
                android:id="@+id/etDetail"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:inputType="textMultiLine"
                android:minLines="3"
                android:maxLength="250" />
        </com.google.android.material.textfield.TextInputLayout>

        <com.google.android.material.textfield.TextInputLayout
            android:id="@+id/tilMobile"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:hint="Your Mobile Number"
            android:layout_marginBottom="20dp">

            <com.google.android.material.textfield.TextInputEditText
                android:id="@+id/etMobile"
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:inputType="phone"
                android:maxLength="11" />
        </com.google.android.material.textfield.TextInputLayout>

        <ProgressBar
            android:id="@+id/progressBar"
            android:layout_width="wrap_content"
            android:layout_height="wrap_content"
            android:layout_gravity="center_horizontal"
            android:visibility="gone" />

        <Button
            android:id="@+id/btnSubmit"
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:text="Submit Grievance" />

    </LinearLayout>
</ScrollView>
```

---

## Step 9 — Navigation Graph (nav_graph.xml additions)

Add these two destinations and actions inside your existing `<navigation>` element:

```xml
<fragment
    android:id="@+id/grievanceListFragment"
    android:name="com.yourapp.fragment.GrievanceListFragment"
    android:label="My Grievances"
    tools:layout="@layout/fragment_grievance_list">

    <action
        android:id="@+id/action_grievanceList_to_grievanceSubmit"
        app:destination="@id/grievanceSubmitFragment" />

    <action
        android:id="@+id/action_grievanceList_to_grievanceDetail"
        app:destination="@id/grievanceDetailFragment">
        <argument
            android:name="grievance_id"
            app:argType="integer" />
    </action>
</fragment>

<fragment
    android:id="@+id/grievanceSubmitFragment"
    android:name="com.yourapp.fragment.GrievanceSubmitFragment"
    android:label="New Grievance"
    tools:layout="@layout/fragment_grievance_submit" />
```

---

## Step 10 — Bottom Navigation / Menu Entry

Add to your existing `bottom_nav_menu.xml` (or wherever the parent menu is):

```xml
<item
    android:id="@+id/grievanceListFragment"
    android:icon="@drawable/ic_grievance"
    android:title="Grievance" />
```

> Use any complaint/flag icon from Material Icons or your existing icon set.

---

## Status Badge Colors (colors.xml)

```xml
<!-- Add to res/values/colors.xml -->
<color name="status_open">#D32F2F</color>        <!-- red -->
<color name="status_pending">#F57C00</color>     <!-- orange -->
<color name="status_inprogress">#1565C0</color>  <!-- blue -->
<color name="status_resolved">#2E7D32</color>    <!-- green -->
```

---

## Quick Reference — Auth Headers

Every call needs:
```
Authorization: Bearer <access_token>
?username=<student_username>
```

Token is stored in `SharedPreferences` key `"access_token"` (same as all other screens).

---

## Error Handling

| HTTP | Meaning |
|------|---------|
| `400` | Missing/invalid field — show the `error` string from response body |
| `401` | Token expired — refresh using `POST /mobi/api/token/refresh/` |
| `404` | Student not found |
| `201` | Grievance created successfully |
| `200` | OK (GET) |
