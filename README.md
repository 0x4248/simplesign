# Simple Sign

Easily sign or hash text messages using your private key and sha265 or any hashing algorithm.

## Configuration

To start the setup run 

```
python -m simplesign
```

Simple sign will ask you if you want to setup and then will ask you questions like name, email, private key location and hashing algorithm.

## Usage

To sign a message run

```
python -m simplesign
```

This will open up nano and you can write your message there. When you are done press ctrl+x and then y to save and exit.

Or you can run 

```
python -m simplesign -f <file>
```

This will open the file and sign it.