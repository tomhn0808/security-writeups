# captcha Solver
This simple python script will do the following action:

* Retrieve information from an URL (here : "http://mywebsite.com/captcha_page")

* Uses the BeautifulSoupv4 library to parse this HTML and retrieve the base64 encoded data associated with an image. This is contained in a prefixed text: "data:image/png;base64,zqdkozkosd02jd9aja8..."

* Afterwards, the script will save this decoded base64 data into a captcha.png file

* Use the gocr command to retrieve the text encoded in the image (this isn't 100% reliable, multiple test might be required to successfully do it). This command uses "Optical Character Recognition" ([Documentation](https://en.wikipedia.org/wiki/GOCR))

* Send a POST to the same URL (using an opened session to keep the link between the GET and POST response)

* Print the response received from the server after the POST request.