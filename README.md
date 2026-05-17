# Hash Cracker

At first you should have python installed.

In Linux/MacOS go to CLI (Terminal) and write:

Bash

`git clone 
cd Advanced_Hash_Cracker
chmod +x hash_cracker.py`

Now you should know all the commands:

- `-h, --help`
Displays the help menu and shows how to use all available commands.
- `-t, --target`
Specifies the target hash string you want to crack (Supports: MD5, SHA-1, SHA-256, SHA-512).
- `-w, --wordlist`
Specifies the path to your dictionary file (Works perfectly with both small custom lists and heavy databases like rockyou.txt).
- `--threads`
Specifies the number of parallel threads to speed up the process (Default is 20).

**IMPORTANT: Manual Code Modification Required**
Inside the script, the `detect_hash_type` function relies strictly on the character length of the hash to automatically determine the algorithm.

If you are testing custom enterprise hashes, salted variants, or specific encryption lengths that deviate from standard formats, it is **absolutely necessary** to open the `hash_cracker.py` file and manually adjust the length validation constraints inside the loop before executing the tool. Failing to change these hardcoded rules will result in invalid hash length errors.