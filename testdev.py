from django.shortcuts import render, redirect


def age():
    age_people = [("Не указан", "Не указан")]
    age_people.extend([(year, year) for year in range(0, 121)])  # Используйте одну переменную

    print(age_people)

    context = {
        'age_people': age_people
    }

     return render(request, 'create_user.html', context)


