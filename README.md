
# Catan
:game_die: A map generator for Catan, both classic game and extended. 

For now, no seafarers supported, but maybe in the future, it will, who knows.
This was developed with `numpy`, so if you don't have it already, please install it. Amazing tool for probabilities and statistics and all sorts of stuff.

## How to use
#### Download
- First, clone/download the repository: 
`git clone https://github.com/Japjappedulap/Catan.git`

 - Install `numpy` (if you don't already have it): 
 `pip3 install numpy`

 #### Use
 - For generating a classic map, just run `python3 classic.py`. The result should be something like this:

                    DESE 0      OREE 6      LUMB 2	
              GRAI 8      WOOL 3      CLAY10      WOOL 9	
        WOOL12      OREE10      LUMB 6      GRAI11      CLAY 5	
              CLAY 8      GRAI 3      WOOL 4      LUMB 9	
                    LUMB11      OREE 5      GRAI 4	
 
 - For generating an extended map, run `python3 extended.py`. Careful at this one, the map isn't symmetric
 
                          DESE 0      OREE 8      WOOL12      GRAI 8
                    LUMB 9      WOOL11      GRAI 4      OREE 5      LUMB12
              OREE 3      CLAY10      LUMB 6      CLAY 3      GRAI 9     CLAY 6
        CLAY 6      GRAI 4      WOOL 3      OREE10      WOOL 9      LUMB 2
              LUMB11      CLAY 5      LUMB10      GRAI11      OREE 5
                    WOOL 4      GRAI 2      WOOL 8      DESE 0

> **Note**: generations will take time, maybe a lot of time, do not be surprised if you wait 3-4 minutes for an extended map. A classic map should be rendered in no more than one minute.
##### Reading this mess
Each 'entry' consists of a resource tile and a dice number `GRAI 9` means a grain resource tile with a dice of 9 on it.
- `DESE` = Desert, always with 0, no dice on it (duh...) 
- `LUMB` = Lumber 
- `WOOL` = Wool 
- `GRAI` = Grain 
- `OREE` = Ore 
- `CLAY` = Clay 

## Why this?
The maps generated aren't always perfect, but they're getting as close as ever to perfection. The distribution of dice numbers across the resources is extremely balanced. The positioning of all tiles is done such that no place is favored over the other, there is no *really good* spot, most of them are equally good and equally balanced. Of course, it's still the rolled dice which dictates the game, but at least, the map is balanced.

#### Still missing
Even if the tiles placement is great, there is a single lacking feature. The harbor :anchor: configurations. You can still place the tiles rotated as you want, to make the entire map more enjoyable, just don't overdo it.
