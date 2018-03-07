# directory2rss

directory2rss is a small tool that generates an RSS feed from Apache and nginx index pages to notify about changes.
It sets up a small webserver that takes the target URL as parameter and returns the generated RSS feed.

<h1 style="color:red">Disclaimer</h1>

This software has no security measurements and no access control.
It behaves similary to a proxy to everyone that is able to access it.
Do <b>not</b> use it in a public unsecured environment.
Only use run it on a trusted machine in a trusted network (which mostly only applies to localhost).
Also TLS certificates of the target are <b>not</b> checked.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

## Setup

Install the following Python 3 packages through your preferred package manager:

 - `requests`
 - `bs4`
 - `flask`
 - `PyRSS2Gen`

### Configuration

 Look up the code.

## Usage

To start, run `./d2rss.py`.

To add a feed to your preferred feed reader add:
```
http://localhost:5000/?url=<directory url>&user=<basic auth user name>&pass=<basic auth password>
```

`user` and `pass` are only required if the directory index is protected by basic authentication.

### Example

To read a feed of `https://example.com/some_directory` just add `http://localhost:5000/?url=https://example.com/some_directory` to your feed reader.

### Screenshot

![directory2rss on firefox and akregator](https://github.com/jklmnn/directory2rss/raw/master/d2rss.png)
