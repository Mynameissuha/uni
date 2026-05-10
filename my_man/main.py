from manag import FileManager

def main():

    fm = FileManager()

    print("File manager activated")
    print("Type 'help' to see commands list")

    while True:
        rel_path = fm.get_relative_path()
        user_input = input(f"manager://{rel_path} $ ").strip().split()
        
        if not user_input:
            continue
        
        command = user_input[0].lower()
        args = user_input[1:]

        try: 
            if command == "exit":
                print("exiting..")
                break

            elif command == "look":
                items = fm.list_dir()
                for item in items:
                    prefix = "[DIR]" if item.is_dir() else "[FILE]"
                    print(f"{prefix} {item.name}")

            elif command == "go":
                if args:
                    fm.move_to(args[0])
                else:
                    print("Usage: go [folder_name]")
            
            elif command == "create":
                if args:
                    fm.create_dir(args[0])
                else:
                    print("Usage: create [folder_name]")

            elif command == "destroy":
                if args:
                    fm.delete(args[0])
                else:
                    print("Usage: destroy [name]")
            elif command == "clear":
                if args:
                    print("Usage: clear")
                else:
                    fm.clear_screen()
            elif command == "help":
                print("Commands: look, go, create, destroy, exit,clear")

            else:
                print(f"Unknown command: {command}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()