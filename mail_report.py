import webbrowser
import sensetive_info

def open_webmail():
    webmail_url =   sensetive_info.WEBMAIL_LINK# Replace with your webmail URL
    webbrowser.open(webmail_url)

if __name__ == "__main__":
    open_webmail()
