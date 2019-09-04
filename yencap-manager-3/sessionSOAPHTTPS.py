      
import SOAPpy


server = SOAPpy.SOAPProxy("https://localhost:832")
print server.hello()
