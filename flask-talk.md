# Web Development with Flask
Given at Local Hack Day 2015, by Jack Cook

## What is Flask?
Flask is a microframework written in Python for the purpose of developing a website.
For anyone who is new to web development, Flask and other web frameworks are useful because they provide the advantage of processing code on a centralized backend server.

For people who already know Python, Flask is very easy to pick up and integrate with the rest of your code.
Let's get started.

## Installing Flask
As you would do with any other Python package, in order to use Flask, you need to install it with `pip`.
This can be done by entering the following command in your terminal.

`$ pip install flask`

If you get an error that suggests that `pip` may not be installed, you can install it using `easy_install`.

`$ sudo easy_install pip`

## Hello, World!
We're going to begin by making the classic "Hello, world" program.
Fortunately, using Flask is very easy, and does not require very many lines of code.

```python
# As with any other Python library, we're going to need to import the Flask module.
from flask import Flask

# Next, you're going to create your app variable. This variable will allow you to tell Flask how your website should work.
app = Flask(__name__)

# In Flask, requests are retrieved like so:
@app.route("/")
def get_root():
  return "Hello, world!"

# The return value of these methods that you create is what ends up being received by a web browser hitting the page.
# You can create as many of these methods as you would like to have endpoints on your website.

# Lastly, you're going to need to start the Flask process when you run your python script.
# Although not required, for the purposes of this talk, I recommend you turn on debug mode, as it will greatly help you figure out what's wrong if Flask throws an exception.
if __name__ == "__main__":
  app.run(debug=True)
```

If we now run our Python script, we should be able to see our new website.

```
$ python app.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

If we go to the URL that was put in our terminal, we can now see our website.
As we can see, the web browser receives what we returned in the `get_root` method of our Python file.
Because it works this way, you can also edit that method to return HTML.

```python
@app.route("/")
def get_root():
  return "<html><body><p>Hello, world!</p></body></html>"
```

However, this obviously quickly becomes tedious.
As many websites can contain several hundred lines of HTML, not including CSS and JavaScript, you're likely going to want to handle all of this in a way that allows you to edit and deal with it easily. Not by keeping it all in a string in your Python file.
Fortunately, Flask offers a very easy solution to this problem.
Flask is built upon another library known as `jinja2`, which gives us an easy way to manage HTML files with Python.
If we go to back to the import statement at the top of our Python file, we're also going to be importing a function called `render_template`.

```python
from flask import Flask, render_template
```

This function allows us to return a website contained in another file, rather than contained in a string.

Now, we can update our `get_root` method to return data from another file, such as `index.html`.
Because of the way this method works, you're going to need to keep all of your HTML files in a `templates` folder, which Flask will be reading your files from.

```python
@app.route("/")
def get_root():
  return render_template('index.html')
```

```html
<html>
  <body>
    <p>Hello world, from my HTML file!</p>
  </body>
</html>
```

If all goes well, you should be able to refresh your page to see "Hello world, from my HTML file!".
If you see a 500 error in your console or a `jinja2.exceptions.TemplateNotFound` error on your webpage, it is most likely because you mistyped your HTML file name or forgot to put the file in the `templates` folder.

## Dynamic HTML Files

One very useful feature of `jinja2`, the HTML rendering library in Flask, is that you can call Python code straight from your HTML file in order to change content that is displayed on the page.
One practical use of this is the ability to reference CSS and JavaScript files in your HTML code.
Because your HTML file is being served from a separate directory, Flask will not immediately know where to look for your CSS code if you hardcode the filepath in your HTML file.

To call Python code from your HTML file, you can wrap the Python code with curly braces, like so.

```html
<html>
  <head>
    <link href="{{ url_for('static', filename='style.css') }}" rel="stylesheet" />
  </head>
  <body>
    <p>Hello world, from my HTML file!</p>
  </body>
</html>
```

The important part to note here is that you are literally calling Python code by doing this.
Here, `url_for` is a Python method that is being called.
`url_for` is another method provided by `jinja2`, and can be imported at the top of our Python file.

```python
from flask import Flask, render_template, url_for
```

If we go back to the `url_for` method being called in our HTML file, we can see that the first parameter is `static`.
This tells Flask that it should look for the file named `style.css` in a folder called `static`.
So we're going to do exactly that.
Create a new folder in the same directory as the rest of your files and call it "static".
In that folder, create a file called `style.css`.
Here, you can place all of your CSS rules that are displayed in your HTML file.

```css
body {
  background: #009688;
}

p {
  color: #fff;
}
```

If we run our `app.py` file now, everything should work as expected, and you should see a page like this.
Our HTML page is working and stylized.

Serving Python code to your HTML files can serve many other useful purposes as well, especially if you are trying to serve dynamic content across sessions on your website.
The `render_template` function accepts any key with any value.
Because of this, as long as your variable yields data that can be displayed in the form of a string, it can be displayed in your HTML file.

```python
@app.route("/")
def get_root():
  stock_price = 75.43
  return render_template('index.html', data=stock_price)
```

You would then refer to that data using the name of the key (not the value) in the HTML file.

```html
<p>The current price of this stock is {{ data }}</p>
```

## URL Handling
In Flask, it is very easy to add new endpoints.
All you have to do is add another route to the `app` variable, and return more data.

```python
@app.route("/")
def get_root():
  return render_template('index.html')

@app.route("/data")
def get_data():
  return render_template('other_file.html')
```

For more advanced HTTP uses, you can also receive requests that are not `GET` requests.
For example, if you wanted to receive a `POST` request, just add a `methods` parameter to the `route` function.

```python
@app.route("/data", methods=["POST"])
def post_data():
  return "Your data has been received!"
```

If you are receiving data through a POST request, you are likely going to want to be able to read URL parameters or HTTP headers.
This can be done easily as well.

To read URL parameters, we're going to need to import another part of the Flask library, the `request` variable.

```python
from flask import Flask, render_template, url_for, request

# Once you've imported the request variable, you can very easily read URL parameters.
@app.route("/data", methods=["POST"])
def post_data():
  query = request.args.get('q')
  print "Query: %s" % query

  # If the URL were http://localhost/data?q=myquery, query would be equal to "myquery"
  # Don't forget that you still need to return data, even if the request is not a GET request.

  return "Your data has been received!"
```

To read HTTP headers, we can use a similar method, also utilizing the `request` variable.

```python
@app.route("/data", methods=["POST"])
def post_data():
  auth = request.headers.get('Authorization')
  print auth
  return "Your data has been received!"
```
