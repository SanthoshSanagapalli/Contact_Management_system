
import os

def load_contacts(filename):
    """Load contacts from CSV (name,phone). Return dict."""
    contacts = {}
    if not os.path.exists(filename):
        return contacts
    try:
        f = open(filename, "r")
    except Exception:
        return contacts
    for line in f:
        line = line.strip() 
        if not line:
            continue
        parts = line.split(",", 1)
        if len(parts) != 2:
            continue
        name = parts[0].strip()
        phone = parts[1].strip()
        if name:
            contacts[name] = phone
    f.close()
    return contacts

def save_contacts(contacts, filename):
    """Save contacts dict to CSV. Return True on success."""
    try:
        f = open(filename, "w")
    except Exception:
        return False
    for name, phone in contacts.items():
        # replace commas to keep CSV safe
        safe_name = name.replace(",", " ")
        safe_phone = str(phone).replace(",", " ")
        f.write(safe_name + "," + safe_phone + "\n")
    f.close()
    return True

def add_contact(contacts, name, phone):
    """Add a contact. If exists, returns False. Otherwise adds and returns True."""
    key = name.strip()
    if key == "":
        return False, "Name cannot be empty."
    # normalize phone: remove spaces
    phone_norm = phone.strip()
    if key in contacts:
        return False, "Contact already exists. Use update to change phone."
    contacts[key] = phone_norm
    return True, "Added."

def update_contact(contacts, name, phone):
    """Update existing contact. Returns (bool, message)."""
    key = name.strip()
    if key == "":
        return False, "Name cannot be empty."
    if key not in contacts:
        return False, "Contact not found."
    contacts[key] = phone.strip()
    return True, "Updated."

def delete_contact(contacts, name):
    """Delete contact by name. Returns (bool, message)."""
    key = name.strip()
    if key in contacts:
        contacts.pop(key)
        return True, "Deleted."
    return False, "Contact not found."

def search_contact(contacts, query):
    """Search by substring (case-insensitive) in names. Return list of (name,phone)."""
    q = query.strip().lower()
    if q == "":
        return []
    results = []
    for name, phone in contacts.items():
        if q in name.lower():
            results.append((name, phone))
    return results

def display_contacts(contacts):
    """Return a formatted string of all contacts sorted by name."""
    if not contacts:
        return "No contacts stored."
    lines = []
    for name in sorted(contacts.keys(), key=lambda s: s.lower()):
        lines.append(f"{name:<20} | {contacts[name]}")
    return "\n".join(lines)

def demo_sample_contacts():
    """Small helper to return a sample contacts dict for quick demo/testing."""
    return {
        "Anika": "9876543210",
        "Bharat": "9123456780",
        "Charu": "9988776655"
    }

# --- Interactive menu (uses the functions above) ---
def main():
    FNAME = "contacts.csv"
    contacts = load_contacts(FNAME)

    while True:
        print("\nContact Manager")
        print("1. Add contact")
        print("2. Update contact")
        print("3. Delete contact")
        print("4. Search contacts")
        print("5. Display all")
        print("6. Save contacts")
        print("7. Load sample contacts (demo)")
        print("8. Quit")
        choice = input("Choose (1-8): ").strip()

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            ok, msg = add_contact(contacts, name, phone)
            print(msg)
        elif choice == "2":
            name = input("Name to update: ")
            phone = input("New phone: ")
            ok, msg = update_contact(contacts, name, phone)
            print(msg)
        elif choice == "3":
            name = input("Name to delete: ")
            ok, msg = delete_contact(contacts, name)
            print(msg)
        elif choice == "4":
            q = input("Search query (part of name): ")
            res = search_contact(contacts, q)
            if not res:
                print("No matches.")
            else:
                for n, p in res:
                    print(f"{n:<20} | {p}")
        elif choice == "5":
            print("\nAll contacts:")
            print(display_contacts(contacts))
        elif choice == "6":
            fname = input(f"Filename to save [{FNAME}]: ").strip()
            if fname == "":
                fname = FNAME
            if save_contacts(contacts, fname):
                print("Saved to", fname)
            else:
                print("Save failed.")
        elif choice == "7":
            contacts = demo_sample_contacts()
            print("Sample contacts loaded.")
        elif choice == "8":
            # ask to save before exit
            ans = input("Save before exit? (y/n): ").strip().lower()
            if ans == "y":
                save_contacts(contacts, FNAME)
                print("Saved.")
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Enter 1-8.")

if __name__ == "__main__":
    main()
