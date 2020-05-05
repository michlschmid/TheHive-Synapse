title = "[THE HIVE] - Case: #"

async def sendEmail(self, params: AttrDict, setting: AttrDict):
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        autoescape=select_autoescape(['html', 'xml'])
    )

    env.globals['any'] = any
    env.globals['int'] = int

    text_template = env.get_template("sendEmail.jinja2.txt")

    debug("params", params)

    # Required
    database = params['database']
    subject = params['subject']
    receipients = [r.strip() for r in params['receipients'] if r.strip()]
    receipients_cc = [r.strip() for r in params['receipients_cc'] if r.strip()]

    log.info("Rendering report as text and XML")
    template_data = {
        "cause": params['cause'],
        "comment": params['comment'],
        "police": params.get('police', False),
        "fireservice": params.get('fireservice', False),
        "rescueservice": params.get('rescueservice', False),
        "thw": params.get('thw', False),
        "now": datetime.now(tz=LOCAL_TZ),
    }
    text_message = text_template.render(**template_data)

    #
    # Build email
    #

    try:
        host = settings['smtp.host']
        port = settings['smtp.port']
        enforce_tls = settings['smtp.enforce_tls']
        username = settings['smtp.username'] # Can be empty
        password = settings['smtp.password'] # Can be empty
        sender_name = settings['smtp.default-sender-name']
        sender_email = settings['smtp.default-sender-email']
        subject_prefix = settings['smtp.subject-prefix']
    except KeyError as e:
        raise Exception(f"Missing configuration value {e}. Please check your SMTP settings.")

    import smtplib
    from email.message import EmailMessage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # https://docs.python.org/3/library/email.examples.html
    msg = EmailMessage()
    msg['Subject'] = f"{subject_prefix[database]} {subject}"
    msg['From'] = f'"{sender_name}" <{sender_email}>"'
    msg['To'] = ", ".join(receipients)
    msg['Cc'] = ", ".join(receipients_cc)

    msg.set_content(text_message)

    log.info("Connecting to SMTP")
    smtp = smtplib.SMTP(host, port=int(port))
    if enforce_tls:
        smtp.starttls()

    if username and password:
        smtp.login(username, password)

    log.info("Sending message")
    smtp.send_message(msg)

    targets = len(receipients) + len(receipients_cc)
    return f"E-Mail successfully sent to the following recipients: {targets}"
