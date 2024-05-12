# Concepts

## SMTP

In order to configure a scheduled email service some knowledge of SMTP is required.

SMTP is a *procotol* for transmitting and receiving emails over a network. It operates at the 
application layer of the TCP/IP framework.

As an analogy, you can think of it like sending regular mail in real life: we typically provide
the postman with an envelope, an address and a stamp which communicates to the postman that this
is a letter we would like to send to address XYZ and with a speed that accords with the provided
stamp. 

The way it works is that you (the 'client') communiate with an *SMTP server* to distribute emails
across a network. More specifically,

> An SMTP server is an application that connects to an email client 
> (through port 25 or 587, usually) to deliver emails. When you send an email, the email client 
> converts the message into code that specifies the sender’s address, receiver’s address, and 
> the contents of the email.

To facilitate communication the protocol specifies a certain number of commands,

* HELO: Identifies the email sender’s server and domain name
* MAIL FROM: Specifies the sender’s email address
* RCPT: Identifies the email’s recipient
* DATA: This command signals the beginning of the email’s content
* QUIT: Ends the SMTP server connection

## OAuth 2.0

In the schematic presented below, 

* The **Client** is this particular Python application (alias: `pyrise`)
* The **Resource Owner** is one's own Google account (like an embassy, alias: `pyrise.no.reply@gmail.com`)
* The **Authorization Server** is Google's OAuth 2.0 server (like border control)
* The **Resource Server** is Google's Gmail API (like a separate country)

+--------+                               +---------------+
|        |--(A)- Authorization Request ->|   Resource    |
|        |                               |     Owner     |
|        |<-(B)-- Authorization Grant ---|               |
|        |                               +---------------+
|        |
|        |                               +---------------+
|        |--(C)-- Authorization Grant -->| Authorization |
| Client |                               |     Server    |
|        |<-(D)----- Access Token -------|               |
|        |                               +---------------+
|        |
|        |                               +---------------+
|        |--(E)----- Access Token ------>|    Resource   |
|        |                               |     Server    |
|        |<-(F)--- Protected Resource ---|               |
+--------+                               +---------------+