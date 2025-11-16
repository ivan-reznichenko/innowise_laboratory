def generate_profile(age):
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    else:
        return "Adult"

while True:
    user_name = input("Enter your full name: ").strip()
    if user_name:
        break
    print("Name cannot be empty. Please enter your full name.")

while True:
    birth_year_str = input("Enter your birth year: ").strip()
    if not birth_year_str:
        print("Year cannot be empty. Please enter a valid year (e.g., 1990).")
        continue
    try:
        birth_year = int(birth_year_str)
        if 1900 <= birth_year <= 2025:
            break
        else:
            print("Please enter a realistic birth year between 1900 and 2025.")
    except ValueError:
        print("Invalid input. Please enter a numeric year (e.g., 1995).")

current_age = 2025 - birth_year

hobbies = []
print()

while True:
    hobby = input("Enter a favorite hobby or type 'stop' to finish: ").strip()
    if hobby.lower() == "stop":
        break
    if hobby:
        hobbies.append(hobby)
    else:
        print("Hobby cannot be empty. Please enter a hobby or type 'stop'.")

life_stage = generate_profile(current_age)

user_profile = {
    "name": user_name,
    "age": current_age,
    "stage": life_stage,
    "hobbies": hobbies
}

print("\n---")
print("Profile Summary:")
print(f"Name: {user_profile['name']}")
print(f"Age: {user_profile['age']}")
print(f"Life Stage: {user_profile['stage']}")

if not hobbies:
    print("You didn't mention any hobbies.")
else:
    print(f"Favorite Hobbies ({len(hobbies)}):")
    for h in hobbies:
        print(f"- {h}")
print("---")