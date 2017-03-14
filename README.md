# BlindRef v0.2 #
BlindRef serves as the basis for an automated Blind-Based XXE Exploitation Framework

**Usage:**

BlindRef_Attacker.py -s serverURL -p serverPort -r webRequest

**How to use:**

This framework does not currently detect XXE vulnerabilities on its own. BlindRef is designed to be used after successfully discovering the vulnerability within an application.

Upon detecting the ability to resolve external entities:
1. Use the 'Copy as requests' extension from BurpSuite.
2. Paste the output into a file, an example has been included within the code base 'sampleRequest.py'
3. Replace the payload position you discovered with 'BLINDREF'.

BlindRef will then automate the process of enumerating directory structures and files etc.

The operation has two components: BlindRef_Server and BlindRef_Attacker

1. BlindRef_Server: The 'brain' of the operation that hosts and serves entities to the vulnerable web application.
2. BlindRef_Attacker: Instantiates requests to the vulnerable web server to kick off requests for entities hosted on the BlindRef_Server.

These components can reside on separate boxes (additional enhancements will be made to this).

