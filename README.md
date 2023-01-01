# ESG Engine
ESG Engine (Extremely Simple Game Engine) is a little Pygame based game engine which allow you to create online (or not) games really quikly and easily.
You can create a server with very few lines.

## How to make a client ?

### Create a client

You can create a client by inherit a class from the core.client.client_core.Client class, or you can simply create a Client object:

Example :
```python
from ESG_Engine.client.client_core import Client


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
```

or without classes :

```python
from ESG_Engine.client.client_core import Client


client = Client((500, 500))
```

### Game loop

Next, you have to create a game loop which contain the client.tick() function and the client.render() function.

```python
from ESG_Engine.client.client_core import Client


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
    
    def main_loop(self):
        while True:
            self.tick()
            self.render()
```

Before starting your game you need to import the map, the bg (optionnal) and the tileset.

### Import a map, backgrounds and tiles

The map json is made of "width" key, a "height" key and a "layers" key which is a list that contains the tiles (0 is nothing)

Example for a 3 x 3 empty map :

```json
{
  "width" : 3,
  "height" : 3,
  "layers" : [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]
}
```

Note that the first layer is behind the player, the third is in front of the player and the second is used for collisions.

You can import the map with the `client.map.load_from_json(json)` function.


You can register the tileset using the `client.renderer.register_tile(tile_image)` function in a for loop for example.

Finally, you can register the backgrounds using `register_background(parralax, background_image)`. The parralax argument is how far is the background (-1 is no parralax).

So you can import all of that like this :

```python
from ESG_Engine.client.client_core import Client
import pygame


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
    
    def load_map(self):
        with open("my_map.json") as file:
            self.map.load_from_json(file.read())
            file.close()
    
    def load_tiles(self):
        for i in range(64):
            self.renderer.register_tile(pygame.image.load("tile" + str(i) + ".png"))
    
    def load_backgrounds(self):
        self.renderer.register_background(-1, pygame.image.load("background 1.png"))
        self.renderer.register_background(2, pygame.image.load("background 2.png"))
        self.renderer.register_background(6, pygame.image.load("background 3.png"))
```

### Create a player

We can now add a player, and we need to register it:

```python
import pygame
from ESG_Engine.client.client_core import Client
from ESG_Engine.client.player import Player


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
        self.player: Player = self.entity_manager.add_entity(Player(50, 200, 30, 175))
        self.player.set_collider_points([(0, 0), (16, 16), (0, 16), (16, 0)])
        
        self.event_handler.register_event(pygame.KEYDOWN, self.player.player_control_key_down)
        self.event_handler.register_event(pygame.KEYUP, self.player.player_control_key_up)
```

Note that the `add_entity()` function return the given entity.

The last 2 lines are for event handler. See the next section for more explanation.

To add an animation to the player (or Entity), you need a `Anim` object wich contain all the frames of the annimation and bind it to the player into the renderer:

```python
import pygame
from ESG_Engine.client.client_core import Client
from ESG_Engine.client.player import Player
from ESG_Engine.client.animation import Anim


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
        self.player: Player = self.entity_manager.add_entity(Player(50, 200, 30, 175))
        self.player_anim_1 = Anim(0.4)  # take the time between 2 frames
        self.renderer.bind_anim(self.player, self.player_anim_1)
    
    def load_animations(self):
        for i in range(4):
            self.player_anim_1.add_frame(pygame.image.load("player_anim_" + str(i) + ".png"))
```

## Camera

The camera represent the view of the user. The camera is already created in the client object, but we can move it :
```python
from ESG_Engine.client.client_core import Client


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
        self.camera.x = 50
        self.camera.y = 100
```

A better way to move the camera is to modify `camera.target_x` and `camera.target_y`.
You can configure how smooth is the camera's moving with `camera.smooth = value`.
You can also change `camera.zoom` and `camera.lock` (to lock all the camera's movings).

```python
from ESG_Engine.client.client_core import Client


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
        self.camera.target_x = 50
        self.camera.target_y = 100
```

### Event handler

The player object is a simple Entity object the only difference is that the player's controls are already built-in in the player.
So we need to add the players controls into the event_handler with `self.event_handler.register_event(pygame.KEYDOWN, self.player.player_control_key_down)` and `self.event_handler.register_event(pygame.KEYUP, self.player.player_control_key_up)`.

You can add all the events you want in the event handler. When the event handler call a registered function, it gives the pygame event object to the registered function. So your function should be like this :
```python
import pygame
from ESG_Engine.client.client_core import Client


def my_function(event):
    if event.key == pygame.K_SPACE:
        print("Space pressed !")

client = Client((500, 500))

client.event_handler.register_event(pygame.KEYDOWN, my_function)

# Game loop
```

### Clock

The clock object allows you to automatically get the FPS (number of frames per second) and the delta time (time elapsed between 2 frames).
You can also register function that will be repeated each given delays (in second) :

```python
from ESG_Engine.client.client_core import Client


def print_hello():
    print("hello everyone !")

class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
        self.clock.register_task(2., print_hello)
    
    def main_loop(self):
        while True:
            self.tick()
            self.render()
            print("FPS :", self.clock.get_fps(), "Delta time :", self.clock.last_delta)
```
Note that the `self.clock.get_delta()` function return the delta time, but it also resets the delta time. This function is already calles if `core.tick()` so prefer to use `core.clock.last_delta`.

### Particles

You can create and render particles easily using a ParticleEmitter object. This object represent a group of same particles. You can give to it :
- the particle emission area with x, y, width and height
- the maximum speed of a particle (the speed will be between 0 and your given speed)
- the maximum lifetime of a single particle (the lifetime will be between 0 and your given lifetime)
- the texture wich is an animation (the particle annimation will start at a random frame of the animation)

You can also add some extra speed in the direction you want :

```python
from ESG_Engine.client.client_core import Client
from ESG_Engine.client.particles_emitter import ParticlesEmitter
from ESG_Engine.client.animation import Anim

smoke_anim = Anim(0.2)  # Add some frames next to that

client = Client((500, 500))

smoke_emitter = client.particles_emitters_manager.add_particles_emitter(ParticlesEmitter(10, 10, 16, 16, 10, 2, smoke_anim))
smoke_emitter.extra_up = 100
smoke_emitter.extra_right = 50
```

As you can see, we must register our particle into the `client.particles_emitters_manager` object with the `add_particles_emitter()` function (this function return the given particle emitter).

To create particles we need to call the `particle_emitter.create_particles(nbr):` function. The "nbr" argument is the number of particles to create.

### Sound

This Engine allows you to make positionnal sound (The sound volume corresponds to how far you are).
Before playing the sound, you need to register it in the SoundManager object.

```python
from ESG_Engine.client.client_core import Client
import pygame


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
        self.sound_manager.register_sound("incredible_sound", pygame.mixer.Sound("mysound.mp3"))
        
        self.sound_manager.play_sound("incredible_sound", 200, (0, 0), (50, 50))
```

You can also modify the sound's volume during its playing with the `sound_manager.set_sound_volume(sound_name, volume, pos, listening_pos)` function.

## Init the network

To make an online game, you need to init the engine network.

With this engine you can make a server at a very high level.
To create and register a packet you need to give it a name and a schema. The schema is a string wich represent the datas stored in the packet. It's conposed of letters wich represent a data :

s : string
i : int (positive and negative)
ui : unsigned int (only positive)
f : float
b: a byte
ba : a byte array

The letters must be separated by "-".

So if we want a packet that contain a string, an usigned int and a float we must do that like this : `"s-ui-f"`
The packets shema must be imperatively the sames client side and server side.

### Init the client side network

Before registering the packets you have to init the client's network with the address and the port :

```python
from ESG_Engine.client.client_core import Client


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
        self.network.init_client("localhost", 9999)
```

To send packets to the server you need to register a new packet :

```python
from ESG_Engine.client.client_core import Client


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
        self.network.init_client(("localhost", 9999))
    
    def register_packets(self):
        self.network.register_new_packet("hello", "s-i-i-f-ba")
        self.network.register_new_packet("another_packet", "i-ui-s-f")
```

To read the incoming packets, you can make a for loop like a pygame event for loop :

```python
from ESG_Engine.client.client_core import Client


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
        self.network.init_client(("localhost", 9999))
    
    def register_packets(self):
        self.network.register_new_packet("hello", "s-i-i-f-ba")
    
    def read_packets(self):
        for packet in self.network.get_packets():
            if packet.name == "hello":
                print("The server say hello !", packet.data)
```

Note that `packet.data` is a list which contain the decoded data.

You can send data to the server using the `client_send_packet_to_server()` function like this :

```python
from ESG_Engine.client.client_core import Client


class MyClient(Client):
    def __init__(self):
        super().__init__((500, 500))
        self.network.init_client(("localhost", 9999))
    
    def register_packets(self):
        self.network.register_new_packet("hello", "s")
    
    def say_hello_to_server(self):
        self.network.client_send_packet_to_server("hello", ["Hello the server !"])  # data argument must be a list
    
```

To close the client's network you just have to call the `client.network.close()` function.
