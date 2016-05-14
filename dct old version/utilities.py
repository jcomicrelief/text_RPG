# Prompts user for yes or no
def yes_or_no(prompt="> "):
    while 1:
        answer = raw_input(prompt)
        answer = answer.strip()
        answer = answer.lower()

        yes = ["yes", "y", "ye"]
        no = ["no", "n", "nope"]

        if answer in yes:
            return True
        elif answer in no:
            return False
        else:
            continue
