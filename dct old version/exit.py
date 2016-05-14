show_menu()
print("Your vision is blurry when you open your eyes, but you're not "
      "worried. After the nightmare of being kidnapped and brought to a "
      "strange house, you doubt that anything is out of the ordinary. "
      "Until your vision clears and you find yourself still in the house.")
# loop infinitely
while True:
    location = rooms[currentRoom]
    loc_obj = location["object"]
    convert_objects()
    show_location()
    # get the player's next 'action'
    # .split() breaks it up into an list array
    # e.g. typing 'go east' would give the list:
    # ['go', 'east']
    action = raw_input("> ").lower().split()

    # if they type 'go' first
    if action[0] == "go":
        # check that they are allowed wherever they want to go
        if action[1] in location:
            # if door is opened
            if location[action[1]]["status"] == "opened":
                # set the current room to the new room
                currentRoom = location[action[1]]
                convert_objects()
            # if door is locked
            elif location[action[1]]["status"] == "locked":
        # refuse

        # there is no door (link) to the new room
        else:
            print("You can't go that way.")

    # if they type 'take' first
    # JCR: need a better way to do this command for multiple items & notes
    elif action[0] == "take":
        # if the room contains an item and the item is the one they want
        if "item" in location and action[1] in location["item"]:
            # add the item to their inventory
            inventory[location["item"][action[1]]["it name"]] = location["item"][action[1]]
            # display a helpful message
            print("You stored the %s." % action[1])
            del location["item"][action[1]]
            if not location["item"]:
                #  delete the item from the room
                del location["item"]
        # otherwise, if the item isn't there to get
        else:
            # tell them they can't get it
            action = " ".join(action[1:])
            print("There's no %s here." % action)

    # if they type 'look' first
    elif action[0] == "look":
        # if they type 'at' second
        if action[1] == "at":
            # if the room contains the object
            if "object" in location and action[2] in loc_obj:
                print(loc_obj[action[2]]["obj desc"])
            else:
                print("There's no %s in this room." % action[2])

        # if they type 'around' second
        elif action[1] == "around":
            # JCR: might add a better way of formatting objects and items
            print(location["rm desc"])
            if "object" in location:
                objects = ", ".join(location["object"].keys())
                print("Searchable objects: %s" % objects)
            if "item" in location:
                print("Available items: %s" % ", ".join(location["item"]))

        # if they type anything else second
        else:
            print("Look where?")

    # if they type 'search' first
    elif action[0] == "search":
        # if the room contains the searchable object
        if "object" in location and action[1] in loc_obj:
            # JCR: probably a better way of writing these two options
            # if the object contains an item
            if "item" in loc_obj[action[1]]:
                convert_items(action[1])
                multyitems = loc_obj[action[1]]["item"]
                # if more than one item in object
                if len(multyitems) >= 2:
                    print("You found: %s. Take them?" % ", ".join(multyitems.keys()))
                else:
                    print("In your search, you find %s. Take it?" % ", ".join(multyitems.keys()))
                ask = yes_or_no()
                if ask:
                    # add the item to their inventory
                    for key, value in multyitems.iteritems():
                        inventory[key] = value
                    # display a helpful message
                    print("You stored: %s." % ", ".join(multyitems.keys()))
                    # delete the item from the room
                    del loc_obj[action[1]]["item"]

            # if the object has a note
            elif "note" in loc_obj[action[1]]:
                print("You see a %s. Take it?" % loc_obj[action[1]]["note"]["nt desc"])
                ask = yes_or_no()
                if ask:
                    journal[loc_obj[action[1]]["note"]["title"]] = loc_obj[action[1]]["note"]["text"]

            # if the object has both note and item
            # JCR: WIP


            # otherwise there's nothing to find
            else:
                # WIP: provide other sayings to randomly be selected
                print("Nothing of interest here.")

        # otherwise there's nothing to find
        else:
            print("There is no %s here." % action[1])

    # if they type 'drop' first
    elif action[0] == "drop":
        # JCR: How to make "drop" drop the item key and value
        # if the inventory contains the drop-able object
        if action[1] in inventory:
            print("You dropped the %s." % action[1])
            if not "item" in location:
                location["item"] = {}
            location["item"][items[action[1]]["it name"]] = items[action[1]]
            del inventory[action[1]]
        else:
            print("You can't drop something you don't have.")

    # if they type 'read' first
    elif action[0] == "read":
        # if they type 'journal' second
        if action[1] == "journal":
            # check if journal is not empty
            if journal != {}:
                print("\n".join(journal.keys()).title())
            else:
                print("Your journal is empty.")
        elif action[1] in journal:
            print(journal[action[1]])
        else:
            print("Read what?")

    # if they type 'check' first
    elif action[0] == "check":
        # if they type 'inventory' second
        if action[1] == "inventory":
            # check if inventory is not empty
            if inventory != {}:
                print("In your inventory:")
                print("\n".join(inventory.keys()))
            else:
                print("There's nothing in your inventory.")
        elif action[1] in inventory:
            print(inventory[action[1]]["it desc"])
        else:
            print("Check what?")

    # if they type 'quit', they quit the game
    elif action[0] == "quit" and len(action) <= 1:
        break

    # if they type 'help', list the available commands
    # JCR: clearly WIP since it just quits
    elif action[0] == "help" and len(action) <= 1:
        print("Commands:")
        print("'go [direction]'")
        print("'take [item]'")
        print("'drop [item]'")
        print("'look around' or 'look at [object]'")
        print("'search [object]'")
        print("'read journal' or 'read [note]'")
        print("'help'")
        print("'quit'")

    else:
        # WIP: provide other sayings to randomly be selected
        # JCR: probably shouldn't be putting so much effort here...
        # converts the list of action together as a string
        action = " ".join(action)
        print("You can't %s." % action)
        continue
        # roll = randint(0,6)
        # if roll == 0:
        #    print("You don't know how to %s." % action)
        # elif roll == 1:
        #    print("Oh, so you think you can %s. How cute." % action)
        # elif roll == 2:
        #    print("Quit trying to %s. You're embarrassing yourself." % action)
        # elif roll == 3:
        #    print("You can't %s." % action)
        # elif roll == 4:
        #    print("Why would you try to %s?" % action)
        # elif roll == 5:
        #    print("Sorry, doesn't work like that.")
        # elif roll == 6:
        #    print("Wow, good job failing that.")
        # else:
        #     pass