def read_words(file_name: str) -> None:
    """
    Open and read a text file, parse the contents and print each line without list brackets.
    """
    try:
        with open(file_name, "r") as a_file:
            for line in a_file:
                elements = line.strip().split(',')  # Split the line by commas
                print(",".join(elements), end=",")
    except FileNotFoundError as error:
        print(f"File not found: {error}")

def main():
    # Read words from file and print them without list brackets
    file_name = "thing_to_convert.txt"
    read_words(file_name)

if __name__ == "__main__":
    main()
