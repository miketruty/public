# Python hello world for Cloudflare Workers

Your Python code in [index.py](https://github.com/cloudflare/python-worker-hello-world/blob/master/index.py), running on Cloudflare Workers.

In addition to [Wrangler](https://github.com/cloudflare/wrangler) and [npm](https://www.npmjs.com/get-npm), you will need to install [Transcrypt](http://www.transcrypt.org/docs/html/installation_use.html), including Python 3.7 and virtualenv.

#### Wrangler

To generate using [wrangler](https://github.com/cloudflare/wrangler)

```
wrangler generate projectname https://github.com/cloudflare/python-worker-hello-world
```

Further documentation for Wrangler can be found [here](https://developers.cloudflare.com/workers/tooling/wrangler).

#### Transcrypt

Before building your project, you'll need to do one-time setup of Transcrypt.  Assuming you have Python 3.7 and virtualenv installed per the linked instructions above,

```
cd projectname

virtualenv env

source env/bin/activate

pip install transcrypt
```

After that you can run Wrangler commands, such as `wrangler publish` to push your code to Cloudflare.  If you exit virtualenv (`deactivate`) and return to the project directory later, you'll need to activate virtualenv (`source env/bin/activate`) but will not need to rerun the other installation commands.

For more information on how Python translates to Javascript, see the [Transcrypt docs](http://www.transcrypt.org/documentation).

## Truty comments 2020-07-30

I had problems with the instructions online. I also dislike the formatting/style of the Python code used in examples.
I fixed up both, but the Python code needs more work. I need to get a router to show; this needs to look more
like vanilla Django/Flask/Bottle/etc. router code.

Also, the instructions need to be more like this:

```
virtualenv -p /usr/bin/python3 env
source ./env/bin/activate
pip3 install transcrypt
wrangler build
wrangler publish
```

