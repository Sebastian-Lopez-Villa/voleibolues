import requests
import sett
import json
import time

def obtener_Mensaje_whatsapp(message):
    if 'type' not in message :
        text = 'mensaje no reconocido'
        return text

    typeMessage = message['type']
    if typeMessage == 'text':
        text = message['text']['body']
    elif typeMessage == 'button':
        text = message['button']['text']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'list_reply':
        text = message['interactive']['list_reply']['title']
    elif typeMessage == 'interactive' and message['interactive']['type'] == 'button_reply':
        text = message['interactive']['button_reply']['title']
    else:
        text = 'mensaje no procesado'
    
    
    return text

def enviar_Mensaje_whatsapp(data):
    try:
        whatsapp_token = sett.whatsapp_token
        whatsapp_url = sett.whatsapp_url
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer ' + whatsapp_token}
        print("se envia ", data)
        response = requests.post(whatsapp_url, 
                                 headers=headers, 
                                 data=data)
        
        if response.status_code == 200:
            return 'mensaje enviado', 200
        else:
            return 'error al enviar mensaje', response.status_code
    except Exception as e:
        return e,403
    
def text_Message(number,text):
    data = json.dumps(
            {
                "messaging_product": "whatsapp",    
                "recipient_type": "individual",
                "to": number,
                "type": "text",
                "text": {
                    "body": text
                }
            }
    )
    return data

def buttonReply_Message(number, options, body, footer, sedd,messageId):
    buttons = []
    for i, option in enumerate(options):
        buttons.append(
            {
                "type": "reply",
                "reply": {
                    "id": sedd + "_btn_" + str(i+1),
                    "title": option
                }
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "buttons": buttons
                }
            }
        }
    )
    return data

def listReply_Message(number, options, body, footer, sedd,messageId):
    rows = []
    for i, option in enumerate(options):
        rows.append(
            {
                "id": sedd + "_row_" + str(i+1),
                "title": option,
                "description": ""
            }
        )

    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {
                    "text": body
                },
                "footer": {
                    "text": footer
                },
                "action": {
                    "button": "Ver Opciones",
                    "sections": [
                        {
                            "title": "Secciones",
                            "rows": rows
                        }
                    ]
                }
            }
        }
    )
    return data

def document_Message(number, url, caption, filename):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "document",
            "document": {
                "link": url,
                "caption": caption,
                "filename": filename
            }
        }
    )
    return data

def sticker_Message(number, sticker_id):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "sticker",
            "sticker": {
                "id": sticker_id
            }
        }
    )
    return data

def get_media_id(media_name , media_type):
    media_id = ""
    if media_type == "sticker":
        media_id = sett.stickers.get(media_name, None)
    #elif media_type == "image":
    #    media_id = sett.images.get(media_name, None)
    #elif media_type == "video":
    #    media_id = sett.videos.get(media_name, None)
    #elif media_type == "audio":
    #    media_id = sett.audio.get(media_name, None)
    return media_id

def replyReaction_Message(number, messageId, emoji):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "type": "reaction",
            "reaction": {
                "message_id": messageId,
                "emoji": emoji
            }
        }
    )
    return data

def replyText_Message(number, messageId, text):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": number,
            "context": { "message_id": messageId },
            "type": "text",
            "text": {
                "body": text
            }
        }
    )
    return data

def markRead_Message(messageId):
    data = json.dumps(
        {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id":  messageId
        }
    )
    return data

def chatbot_logic(text, number, messageId, list):
    if "hola" in text.lower():
        body = "¡Hola! 👋 Bienvenido a Equipo Voleibol UES. ¿Cómo podemos ayudarte hoy?"
        footer = "Equipo Berrendos"
        options = ["⏳Horario", "📍Lugar", "📞Contacto", "🌐Redes Sociales"]

        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1", messageId)
        replyReaction = replyReaction_Message(number, messageId, "✅")
        list.append(replyReaction)
        list.append(replyButtonData)

    elif "horario" in text.lower():
        body = "El horario es de lunes a viernes de 12:00 a 14:00 y de 14:00 a 16:00."
        footer = "Equipo Berrendos"
        
        replyMessage = textMessage(number, body, footer, messageId)
        list.append(replyMessage)

    elif "lugar" in text.lower():
        body = "Entrenamos en el gimnasio central de la UES. ¡Te esperamos!"
        footer = "Equipo Berrendos"
        
        replyMessage = textMessage(number, body, footer, messageId)
        list.append(replyMessage)

    elif "contacto" in text.lower():
        body = "Puedes contactarnos al correo: voleibol.ues@gmail.com o al teléfono: +52 123 456 7890."
        footer = "Equipo Berrendos"
        
        replyMessage = textMessage(number, body, footer, messageId)
        list.append(replyMessage)

    elif "redes sociales" in text.lower():
        body = "¡Síguenos en nuestras redes sociales!\n\n- Facebook: https://www.facebook.com/profile.php?id=61567390613755\n- Instagram: https://www.instagram.com/volleyball.ues.hmo"
        footer = "Equipo Berrendos"
        
        replyMessage = textMessage(number, body, footer, messageId)
        list.append(replyMessage)

    else:
        body = "Lo siento, no entendí tu mensaje. Por favor elige una de las opciones disponibles."
        footer = "Equipo Berrendos"
        options = ["⏳Horario", "📍Lugar", "📞Contacto", "🌐Redes Sociales"]
        
        replyButtonData = buttonReply_Message(number, options, body, footer, "sed1", messageId)
        replyReaction = replyReaction_Message(number, messageId, "❓")
        list.append(replyReaction)
        list.append(replyButtonData)

# Ejemplo de funciones auxiliares
def buttonReply_Message(number, options, body, footer, sectionId, messageId):
    # Simula la creación de un mensaje con botones de respuesta
    return {"type": "buttonReply", "number": number, "options": options, "body": body, "footer": footer, "sectionId": sectionId, "messageId": messageId}

def replyReaction_Message(number, messageId, reaction):
    # Simula la respuesta con una reacción
    return {"type": "reaction", "number": number, "messageId": messageId, "reaction": reaction}

def textMessage(number, body, footer, messageId):
    # Simula un mensaje de texto simple
    return {"type": "text", "number": number, "body": body, "footer": footer, "messageId": messageId}

# Ejemplo de uso
incoming_text = "redes sociales"
incoming_number = "+52 987 654 3210"
incoming_messageId = "msg124"
response_list = []

chatbot_logic(incoming_text, incoming_number, incoming_messageId, response_list)

for response in response_list:
    print(response)




#al parecer para mexico, whatsapp agrega 521 como prefijo en lugar de 52,
# este codigo soluciona ese inconveniente.
def replace_start(s):
    number = s[3:]
    if s.startswith("521"):
        return "52" + number
    elif s.startswith("549"):
        return "54" + number
    else:
        return s
        

