import gmail

def send(excelfile, botuser, botpassword, toemail):
    gm = gmail.GMail(botuser, botpassword)
    msg = gmail.Message('New listings found.', to=toemail, text="See attached spreadsheet of new listings!", attachments=[excelfile])
    gm.send(msg)