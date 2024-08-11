from cryptography.fernet import Fernet
import os

title = "*** Cryptage Files "
version = "V1.0 *** "
print(title, version)

def menu(): # Fonction principal MENU 

    print()
    print(" --------------------------")
    print("|  Encrypting to File [1]   |")
    print("|  Encrypt Directory !! [2] |") 
    print("|  Decrypt a File [3]       |")
    print("|  Decrypt Directory [4]    |")
    print("|  Look Your SecretKey [5]  |")
    print(" --------------------------")
    print()

    choice = input("Select Your Choice --> ").strip() # Choix of User

    if choice not in ["1", "2", "3", "4", "5" ]: # Si ce n'est pas 1,2,3,4 ou 5 affiche une erreur
        input("Error, Press Enter for Retry...")
        return menu()
    
    if choice == "1":
        crypt_file()
    
    elif choice == "2":
        crypt_directory()

    elif choice == "3":
        decrypt_file()
    
    elif choice == "4":
        decrypt_directory()
    
    elif choice == "5":
        look_secretkey()
    
    else:
        print("Invalid choice")  
        input("Press Enter for Retry...")
        return menu()

def generate_key_register(): # Crée une clé et l'enregistre dans le fichier 'secret.key'
    
    key = Fernet.generate_key() # Variable key stock la clé
    with open("secret.key", "wb") as key_file: # On Ouvre le fichier secret.key en écriture(w) binaire(b) et on l'assigne à key_file
        key_file.write(key) # On écrit le contenue de key_file de key
    print()    
    print("**** WARNING! DON'T LOSE YOUR KEY ! ****")
    input()

def load_key(): # Charge une clé à partir d'un fichier choisi par l'utilisateur
    
    secret_key = input("Select Your File (secret.key) for continue --> ").strip()
    
    if not os.path.isfile(secret_key): #Vérifie si le chemin d'accès existe
        print('Error, file does not exist or Delete ("") exemple: (C:\\Users\\...\\secret.key), Please retry ')
        input("Press Enter for Retry...")
        return load_key()  # Retourne à la fonction load_key en cas de mauvais chemin d'accès
          
    with open(secret_key, "rb") as key_file:
        key = key_file.read()
    print(f"The Key use for Encrypt/Decrypt is --> {key.decode()}") # .decode sert à la visibilité de la clé
    return key 

def verif_key(): # Verifie si secret.key existe
       
    print()
    if not os.path.isfile("secret.key"):
        print('No key found. Generating a new key...')
        generate_key_register() #Génère la clé s'il elle nexiste pas avec la fonction generate_key_register

def crypt_file():  # Cherche le fichier à chiffrer avec la clé fournie par l'utilisateur
   
    verif_key()

    choice_file = input("Select Your File for Encrypt with key --> ").strip()

    if not os.path.isfile(choice_file): # Verifie si le fichier existe bien a l'aide d'os
        print('Error, file does not exist or Delete ("") exemple: (C:\\Users\\...\\file), Please retry ')
        input("Press Enter for Retry...")
        return crypt_file()
    
    secret_key = load_key() # Charge un clé
    if secret_key is None:
        return
     
    with open(choice_file, "rb") as file_to_encrypt:
        file_data = file_to_encrypt.read()
    
    fernet = Fernet(secret_key)
    encrypted_data = fernet.encrypt(file_data)

    with open(choice_file, "wb") as encrypted_file: # Encrypt le fichier dans choice_file avec la clé stocké dans encrypted_data
        encrypted_file.write(encrypted_data)
        
    print(f"Your file {choice_file} is now Encrypted") 
    input("Press Enter to exit")

def crypt_directory(): # Séléction le répertoire à crypté 

    verif_key()
    
    directory_path = input("Select Your Directory for Encrypt with key --> ").strip()
    
    if not os.path.isdir(directory_path):
        print('Error, directory does not exist. Please retry ')
        input("Press Enter for Retry...")
        return crypt_directory()
    
    secret_key = load_key()
    if secret_key is None:
        return
    
    for root, dirs, files in os.walk(directory_path): # os.walk génère tous les noms de fichiers du répertoire
        for file in files:
            file_path = os.path.join(root, file)
            try:
                print(f"Encrypting file: {file_path}")
                crypt_file_path(file_path, secret_key)
            except Exception as e:
                print(f"Error encrypting {file_path}: {e}")

    print(f"All files in {directory_path} are now encrypted.")
    input("Press Enter to exit")

def crypt_file_path(file_path, secret_key): # Chiffre un répertoire

    with open(file_path, "rb") as file_to_encrypt: # Ouvre le répertoire de file_path et l'assigne à file_to_encrypt
        file_data = file_to_encrypt.read() # file_data prends la valeur de file_to_encrypt
    
    fernet = Fernet(secret_key) # Charge la clé de cryptage
    encrypted_data = fernet.encrypt(file_data) # Crypt le répertoire de file_data avec fernet.encrypt
    
    with open(file_path, "wb") as encrypted_file: # le répertoire file_data en ecriture (w) est assigné à encrypted_file
        encrypted_file.write(encrypted_data) # Ecrit les données d'encrypted_file avec les données de encrypted_data (repertoire crypté)

def decrypt_file():

    verif_key()

    file = input("Select Your Encrypted File to Decrypt it --> ").strip()

    if not os.path.isfile(file): # Vérifie si le fichier existe bien a l'aide d'os
        print('Error, file does not exist or Delete ("") exemple: (C:\\Users\\...\\file), Please retry ')
        input("Press Enter for Retry...")
        return decrypt_file()
    
    secret_key = load_key()
    if secret_key is None:
        return
    
    with open(file, "rb") as file_to_decrypt:
        file_data = file_to_decrypt.read()
    
    fernet = Fernet(secret_key)
    decrypted_data = fernet.decrypt(file_data)

    with open(file, "wb") as decrypt_file:
        decrypt_file.write(decrypted_data)
    print(f"Your file {file} is now Decrypted")
    input("Press Enter to exit")

def decrypt_directory():

    verif_key()

    directory_path = input("Select Your Directory to Decrypt --> ").strip()
    
    if not os.path.isdir(directory_path):
        print('Error, directory does not exist. Please retry ')
        input("Press Enter for Retry...")
        return decrypt_directory()
    
    secret_key = load_key()
    if secret_key is None:
        return
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                print(f"Decrypting file: {file_path}")
                decrypt_file_path(file_path, secret_key)
            except Exception as e:
                print(f"Error Decrypting {file_path}: {e}")

    print(f"All files in {directory_path} are now decrypted.")
    input("Press Enter to exit")

def decrypt_file_path(file_path, secret_key): 

    with open(file_path, "rb") as file_to_decrypt:
        file_data = file_to_decrypt.read()
    
    fernet = Fernet(secret_key)
    decrypted_data = fernet.decrypt(file_data)
    
    with open(file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)

def look_secretkey(): # Affiche la SecretKey (clé) (secret.key)

    try: 
       with open('secret.key', 'rb') as file:
           contenu = file.read()
           print(contenu.decode())
           input("Press Enter...")
    
    except Exception as e: # Gère les eventuels erreur et les affiches avec {e}
       print(f"Error,Check that Your SecretKey has been Generated Correctly {e}")

menu() 
