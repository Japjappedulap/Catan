
# Catan
:game_die: A map generator for Catan, both classic game and extended. 

For now, no seafarers supported, but maybe in the future it will, who knows.
This was developed with `numpy`, so if you don't have it already, please install it. Amazing tool for probabilities and statistics and all sorts of stuff.

## How to use
#### Download
- First, clone/download the repository: 
`git clone https://github.com/Japjappedulap/Catan.git`

 - Install `numpy` **(optional)**: 
 `pip3 install numpy`

 #### Use
 - For generating a classic map, just run `python3 classic.py`
 - For generating a extended map, run `python3 extended.py`
 

> **Note**: generations will take time, maybe a lot of time, do not be surprised if you wait 3-4 minutes for an extended map. A classic map should be rendered in no more than one minute.
## Why this?
The maps generated aren't always perfect, but they're getting as closest as ever to perfection. The distribution of dice numbers across the resources is extremely balanced. The positioning of all tiles is done such that no place is favored over the other, there is no *really good* spot, most of them are equally good, and equally balanced. Of course, it's still the rolled dice which dictates the game, but the map is equally balanced.

#### Still missing
Even if the tiles placement is great, there is a single lacking feature. The harbor :anchor: configurations. You can still place the tiles rotated as you want, to make the entire map more enjoyable, just don't overdo it.
