from pushnotify.models import GeneralNotification,temp_GeneralNotification
from mobi.models import DeviceFCMToken
from .models import SectionwiseNotification,SchoolNotification
from admission.models import students
from institutions.models import school
from firebase_admin import messaging
from copy import deepcopy
import datetime





def send_notification(rec_id):
    if isinstance(rec_id, list):
        rec_id = rec_id[0]

    data = temp_GeneralNotification.objects.get(id=rec_id)
    success_count = 0
    total_count = data.post_to.count()
    if data.status == 'Active':
        for client in data.post_to.all():
            std_name = client.first_name + "" + client.last_name
            personalized_message = data.message
            if "{{student_name}}" in personalized_message:
                personalized_message = personalized_message.replace("{{student_name}}", std_name)
            if "{{class_name}}" in personalized_message:
                personalized_message = personalized_message.replace("{{class_name}}", client.class_name.name)

            if DeviceFCMToken.objects.filter(username=client.usernm).exists():
                devices = DeviceFCMToken.objects.filter(username=client.usernm)
                for device in devices:
                    registration_token = device.firecmToken
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title=data.title,
                            body=personalized_message  # Use the updated message
                        ),
                        android=messaging.AndroidConfig(
                            notification=messaging.AndroidNotification(
                                icon=str(data.Notification_school.logo)
                                # Assuming sdata.logo is the name of the icon file in res/drawable
                            )
                        ),
                        token=registration_token,
                    )
                    try:
                        # Send the message and get the response
                        response = messaging.send(message)
                        print("message sent successfully:", response)
                        success_count += 1

                    except Exception as e:
                        # Handle any errors that occur during sending
                        print(f"Error sending notification to {registration_token}: {e}")
    print("total count-successcount",total_count,success_count)
    data.success_count=success_count
    data.total_count = total_count
    data.save()
    new_obj = GeneralNotification.objects.create(
        title=data.title,
        message=data.message,
        create_date=data.create_date,
        post_date=data.post_date,
        created_by_id=data.created_by_id,
        is_read=data.is_read,
        status=data.status,
        Notification_school=data.Notification_school,
        success_count=success_count,
        total_count=total_count
    )
    new_obj.post_to.set(data.post_to.all())
    
def sec_send_notification(rec_id):
    if isinstance(rec_id, list):
        rec_id = rec_id[0]
        try:
            rec = SectionwiseNotification.objects.get(id=rec_id)
            stud = students.objects.filter(class_name=rec.aclass,secs=rec.ssec,school_student=rec.Notification_school)
            title_msg=rec.title_msg
            success_count =0
            total_count = stud.count()
            selected_students = []
            for client in stud:

                # Replace placeholders if they exist in the message content
                std_name = client.first_name + "" + client.last_name
                personalized_message = rec.message_cont
                if "{{student_name}}" in personalized_message:
                    personalized_message = personalized_message.replace("{{student_name}}", std_name)
                if "{{class_name}}" in personalized_message:
                    personalized_message = personalized_message.replace("{{class_name}}", client.class_name.name)

                if DeviceFCMToken.objects.filter(username=client.usernm).exists():
                    devices = DeviceFCMToken.objects.filter(username=client.usernm)
                    for device in devices:
                        registration_token = device.firecmToken
                        message = messaging.Message(
                            notification=messaging.Notification(
                                title=title_msg,
                                body=personalized_message  # Use the updated message
                            ),
                            android=messaging.AndroidConfig(
                                notification=messaging.AndroidNotification(
                                    icon=str(rec.Notification_school.logo)
                                    # Assuming sdata.logo is the name of the icon file in res/drawable
                                )
                            ),
                            token=registration_token,
                        )
                        try:
                            # Send the message and get the response
                            response = messaging.send(message)
                            print("message sent successfully:", response)
                            success_count += 1
                            selected_students.append(client)
                            
                        except Exception as e:
                            # Handle any errors that occur during sending
                            print(f"Error sending notification to {registration_token}: {e}")
            gn = GeneralNotification.objects.create(
                                title=rec.title_msg,message=personalized_message,create_date=rec.create_date,
                                post_date=rec.post_date,created_by_id=rec.created_by,
                                is_read=False,status='ACTIVE',Notification_school=rec.Notification_school,
                                success_count=success_count,total_count=total_count
                            )
            gn.post_to.set(selected_students)            
        except Exception as e:
            # Handle any errors that occur during sending
            print(f"Error sending notification: {e}")
    else:
        print("done completely")


# def school_send_notification(rec_id):
#     if isinstance(rec_id, list):
#         rec_id = rec_id[0]
#         try:
#             rec = SchoolNotification.objects.get(id=rec_id)
#             stud = students.objects.filter(school_student=rec.Notification_school)
#             title_msg = rec.title_msg
#             success_count = 0
#             total_count = stud.count()
#             selected_students = []
#             for client in stud:
#
#                 # Replace placeholders if they exist in the message content
#                 std_name = client.first_name + "" + client.last_name
#                 personalized_message = rec.message_cont
#                 if "{{student_name}}" in personalized_message:
#                     personalized_message = personalized_message.replace("{{student_name}}", std_name)
#                 if "{{class_name}}" in personalized_message:
#                     personalized_message = personalized_message.replace("{{class_name}}", client.class_name.name)
#
#                 if DeviceFCMToken.objects.filter(username=client.usernm).exists():
#                     devices = DeviceFCMToken.objects.filter(username=client.usernm)
#                     for device in devices:
#                         registration_token = device.firecmToken
#                         message = messaging.Message(
#                             notification=messaging.Notification(
#                                 title=title_msg,
#                                 body=personalized_message  # Use the updated message
#                             ),
#                             android=messaging.AndroidConfig(
#                                 notification=messaging.AndroidNotification(
#                                     icon=str(rec.Notification_school.logo)
#                                     # Assuming sdata.logo is the name of the icon file in res/drawable
#                                 )
#                             ),
#                             token=registration_token,
#                         )
#                         try:
#                             # Send the message and get the response
#                             response = messaging.send(message)
#                             print("message sent successfully:", response)
#                             success_count += 1
#                             selected_students.append(client)
#                         except Exception as e:
#                             # Handle any errors that occur during sending
#                             print(f"Error sending notification to {registration_token}: {e}")
#
#             gn = GeneralNotification.objects.create(
#                                 title=rec.title_msg,message=personalized_message,create_date=rec.create_date,
#                                 post_date=rec.post_date,created_by_id=rec.created_by,
#                                 is_read=False,status='ACTIVE',Notification_school=rec.Notification_school,
#                                 success_count=success_count,total_count=total_count
#                             )
#             gn.post_to.set(selected_students)
#         except Exception as e:
#             # Handle any errors that occur during sending
#             print(f"Error sending notification: {e}")
#     else:
#         print("done completely")

from django.db import transaction
from django.utils import timezone
from firebase_admin import messaging

def school_send_notification(rec_id):

    if isinstance(rec_id, list):
        rec_id = rec_id[0]

    # 🔐 LOCK ROW (critical)
    with transaction.atomic():
        rec = (
            SchoolNotification.objects
            .select_for_update()
            .get(id=rec_id)
        )

        # 🛑 STOP duplicates
        if rec.status in ['PROCESSING', 'SENT']:
            return "Already handled"

        rec.status = 'PROCESSING'
        rec.save(update_fields=['status'])

    success_count = 0
    selected_students = []

    try:
        stud = students.objects.filter(
            school_student=rec.Notification_school
        )
        total_count = stud.count()

        for client in stud:
            std_name = f"{client.first_name} {client.last_name}".strip()

            personalized_message = (
                rec.message_cont
                .replace("{{student_name}}", std_name)
                .replace("{{class_name}}", client.class_name.name)
            )

            tokens = DeviceFCMToken.objects.filter(
                username=client.usernm
            )

            for device in tokens:
                try:
                    message = messaging.Message(
                        notification=messaging.Notification(
                            title=rec.title_msg,
                            body=personalized_message
                        ),
                        token=device.firecmToken,
                    )
                    messaging.send(message)
                    success_count += 1
                    selected_students.append(client)

                except Exception as e:
                    print(
                        f"FCM error ({client.usernm}): {e}"
                    )

        # ✅ Create GeneralNotification (NON personalized)
        gn = GeneralNotification.objects.create(
            title=rec.title_msg,
            message=rec.message_cont,
            create_date=rec.create_date,
            post_date=rec.post_date,
            created_by=rec.created_by,
            is_read=False,
            status='ACTIVE',
            Notification_school=rec.Notification_school,
            success_count=success_count,
            total_count=total_count
        )
        gn.post_to.set(selected_students)

        # ✅ MARK AS SENT
        rec.status = 'SENT'
        rec.success_count = success_count
        rec.total_count = total_count
        rec.sent_at = timezone.now()
        rec.save(update_fields=[
            'status',
            'success_count',
            'total_count',
            'sent_at'
        ])

        return "Success"

    except Exception as e:
        rec.status = 'FAILED'
        rec.save(update_fields=['status'])
        raise e   # let Django-Q log it
