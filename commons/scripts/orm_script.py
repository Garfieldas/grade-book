from users.models import User
from commons.models.roles import RoleChoices

def run():
    created = 0
    default_role = RoleChoices.choices[0][0] if getattr(RoleChoices, "choices", None) else "TEACHER"

    for i in range(1, 41):
        first_name = f"User{i}"
        last_name = "Generated"
        email = f"user{i}+generated@example.com"
        is_mentor = (i % 10 == 0)

        user, was_created = User.objects.get_or_create(
            email=email.lower(),
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "role": default_role,
                "is_mentor": is_mentor,
            },
        )
        if was_created:
            created += 1
    print(f"Users processed: 40, created: {created}")