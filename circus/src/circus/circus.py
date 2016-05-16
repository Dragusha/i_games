from random import random
from braser import Braser

DETAIL, DETAILURL = "dungeon_detail", "DungeonWall.jpg"
MONSTER, MONSTERURL = "monster", "monstersheets.png?"
DETILE = "dungeon_detile"
FIRE, FIREURL = "fire", "http://s19.postimg.org/z9iojs2c3/magicfire.png"


class Masmorra:
    def __init__(self):
        self.gamer = Braser(800, 600)
        self.gamer.subscribe(self)
        self.game = self.gamer.game
        self.ph = self.gamer.PHASER
        self.monster = Hero(self.gamer)

    def preload(self):
        # self.game.load.image(DETAIL, DETAILURL)
        self.game.load.spritesheet(MONSTER, MONSTERURL, 64, 63, 16*12)
        self.game.load.spritesheet(DETILE, DETAILURL, 128, 128, 12)
        self.game.load.spritesheet(FIRE, FIREURL, 96, 96, 25)

    def create(self):
        self.game.physics.startSystem(self.ph.Physics.ARCADE)
        self.game.add.sprite(0, 0, DETILE)
        rotate = 0
        for i in range(6):
            for j in range(5):
                detail = self.game.add.sprite(64+i * 128, 64+j * 128, DETILE)
                detail.anchor.setTo(0.5, 0.5)
                detail.angle = rotate
                detail.frame = (6*j+i) % 12
                rotate += 90

        sprite = self.game.add.sprite(148, 148, MONSTER)
        # sprite.animations.add('mon', [7*16+0, 7*16+1, 7*16+2, 7*16+3, 7*16+16 + 0,
        #                               7*16+16 + 1, 7*16+16 + 2, 7*16+16 + 3], 4, True)
        sprite.animations.add('mon', [6*16+0, 6*16+1, 6*16+2, 6*16+3], 4, True)
        sprite.play('mon')

    def update(self):
        pass


class Hero:
    def __init__(self, gamer):
        self.gamer = gamer
        self.gamer.subscribe(self)
        self.game = self.gamer.game
        self.ph = self.gamer.PHASER
        self.monster = self.cursors = self.moves = None

    def create(self):
        # self.game.physics.startSystem(self.ph.Physics.ARCADE)
        sprite = self.game.add.sprite(20, 148, MONSTER)
        # sprite.animations.add('ani', [0, 1, 2, 3, 16+0, 16+1, 16+2, 16+3], 2, True)
        sprite.animations.add('ani', [0, 1, 2, 3], 16, True)
        sprite.play('ani')
        self.game.physics.arcade.enable(sprite)

        # self.game.physics.p2.enable(sprite, False)
        sprite.body.setCircle(28)
        sprite.anchor.setTo(0.5, 0.5)
        sprite.body.collideWorldBounds = True
        # sprite.body.fixedRotation = True
        self.monster = sprite
        self.cursors = crs = self.game.input.keyboard.createCursorKeys()
        self.moves = [(crs.left.isDown, 90, (-150, 0)), (crs.right.isDown, 270, (150, 0)),
                      (crs.up.isDown, 180, (0, -150)), (crs.down.isDown, 0, (0, -150))]

    def preload(self):
        pass

    def update(self):
        cursors, player = self.cursors, self.monster

        #  Collide the player and the stars with the platforms
        # self.game.physics.arcade.collide(self.player, self.platforms)

        player.body.velocity.x, player.body.velocity.y = 0, 0
        player.animations.play('ani')
        # 
        # def mover(angle, direction):
        #     player.angle = angle
        #     player.body.velocity.x, player.body.velocity.y = direction
        #     return True
        # # if not [mover(a, d) for condition, a, d in self.moves if condition]:
        #     player.animations.stop()
        # return

        for move in self.moves:
            if move[0]:
                player.angle = move[1]
                player.body.velocity.x, player.body.velocity.y = move[2]

        if cursors.left.isDown:
            #  Move to the left
            player.angle = 90
            player.body.velocity.x = -150

            # player.animations.play('ani')
        elif cursors.right.isDown:
            #  Move to the right
            player.angle = 270
            player.body.velocity.x = 150

            # player.animations.play('ani')
        elif cursors.up.isDown:
            #  Move to the left
            player.angle = 180
            player.body.velocity.y = -150

            # player.animations.play('ani')
        elif cursors.down.isDown:
            #  Move to the right
            player.angle = 0
            player.body.velocity.y = 150

            # player.animations.play('ani')
        else:
            #  Stand still
            player.animations.stop()


class Main:
    def __init__(self, game, phaser):
        self.ph = phaser
        self.game = game(800, 600, phaser.AUTO, 'flying-circus',
                         {"preload": self.preload, "create": self.create, "update": self.update})
        self.player = self.platforms = self.cursors = self.stars = self.scoreText = None
        self.score = 0
        pass

    def preload(self, *_):
        self.game.load.image('image-url', 'assets/sky.png')

        self.game.load.image('ground', 'assets/platform.png')
        self.game.load.image('star', 'assets/star.png')
        self.game.load.spritesheet('dude', 'assets/dude.png', 32, 48)

    def create(self, *_):
        self.game.physics.startSystem(self.ph.Physics.ARCADE)
        self.game.add.sprite(0, 0, 'image-url')
        self.game.add.sprite(0, 0, 'star')
        platforms = self.game.add.group()
        platforms.enableBody = True
        ground = platforms.create(0, self.game.world.height - 64, 'ground')
        ground.scale.setTo(2, 2)
        ground.body.immovable = True
        ledge = platforms.create(400, 400, 'ground')

        ledge.body.immovable = True

        ledge = platforms.create(-150, 250, 'ground')

        ledge.body.immovable = True

        player = self.game.add.sprite(32, self.game.world.height - 150, 'dude')

        #  We need to enable physics on the player
        self.game.physics.arcade.enable(player)

        #  Player physics properties. Give the little guy a slight bounce.
        player.body.bounce.y = 0.2
        player.body.gravity.y = 300
        player.body.collideWorldBounds = True

        #  Our two animations, walking left and right.
        player.animations.add('left', [0, 1, 2, 3], 10, True)
        player.animations.add('right', [5, 6, 7, 8], 10, True)

        self.cursors = self.game.input.keyboard.createCursorKeys()
        stars = self.game.add.group()

        stars.enableBody = True
        # return

        #  Here we'll create 12 of them evenly spaced apart
        for i in range(12):

            #  Create a star inside of the 'stars' group
            star = stars.create(i * 70, 0, 'star')

            #  Let gravity do its thing
            star.body.gravity.y = 6

            #  This just gives each star a slightly random bounce value
            star.body.bounce.y = 0.7 + random() * 0.2
        self.scoreText = self.game.add.text(16, 16, 'score: 0', dict(fontSize='32px', fill='#000'))
        self.player, self.platforms, self.stars = player, platforms, stars

    def update(self, *_):
        cursors, player, platforms, stars = self.cursors, self.player, self.platforms, self.stars

        #  Collide the player and the stars with the platforms
        self.game.physics.arcade.collide(self.player, self.platforms)

        player.body.velocity.x = 0

        if cursors.left.isDown:
            #  Move to the left
            player.body.velocity.x = -150

            player.animations.play('left')
        elif cursors.right.isDown:
            #  Move to the right
            player.body.velocity.x = 150

            player.animations.play('right')
        else:
            #  Stand still
            player.animations.stop()

            player.frame = 4

        #  Allow the player to jump if they are touching the ground.
        if cursors.up.isDown and player.body.touching.down:
            player.body.velocity.y = -350

        def collectstar(_, star):
            # Removes the star from the screen
            star.kill()
            self.score += 10
            self.scoreText.text = 'Score: %d' % self.score

        self.game.physics.arcade.collide(stars, platforms)

        self.game.physics.arcade.overlap(player, stars, collectstar, None, self)


def circus():
    from browser import doc
    doc["pydiv"].html = PAGE0


def main():
    Masmorra()
    # Main(Game, auto)
print(__name__)
if __name__ == "__main__":
    main()
#main()

PAGE0 = '''
    <div class="related">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="genindex.html" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="inicia.html" title="Primeiro Cenário do Jogo"
             accesskey="N">next</a> |</li>
        <li><a href="#">Flying Circus 0.1.0 documentation</a> &raquo;</li>
      </ul>
    </div>

    <div class="document">
      <div class="documentwrapper">
        <div class="bodywrapper">
          <div class="body">

  <div class="section" id="bem-vindos-ao-circo-voador-da-programacao-python">
<h1>Bem Vindos ao Circo Voador da Programação Python<a class="headerlink" href="#bem-vindos-ao-circo-voador-da-programacao-python" title="Permalink to this headline">¶</a></h1>
<p>Aqui vamos ter uma introdução rápida de como programar jogos para Web usando Python.
Na verdade vamos usar o Brython que é o Python que funciona dentro de um navegador web como o Firefox.</p>
<img alt="http://s19.postimg.org/ufgi8eztf/PPFC.jpg" src="http://s19.postimg.org/ufgi8eztf/PPFC.jpg" />
</div>
<div class="section" id="sumario">
<h1>Sumário<a class="headerlink" href="#sumario" title="Permalink to this headline">¶</a></h1>
<div class="toctree-wrapper compound">
<ul>
<li class="toctree-l1"><a class="reference internal" href="inicia.html">Primeiro Cenário do Jogo</a></li>
<li class="toctree-l1"><a class="reference internal" href="desafio_a.html">Criando uma Câmara com Constantes</a></li>
<li class="toctree-l1"><a class="reference internal" href="desafio_b.html">Posicionando um Personagem com Inteiros</a></li>
</ul>
</div>
</div>
<div class="section" id="indices-e-tabelas">
<h1>Indices e Tabelas<a class="headerlink" href="#indices-e-tabelas" title="Permalink to this headline">¶</a></h1>
<ul class="simple">
<li><a class="reference internal" href="genindex.html"><em>Index</em></a></li>
<li><a class="reference internal" href="py-modindex.html"><em>Module Index</em></a></li>
<li><a class="reference internal" href="search.html"><em>Search Page</em></a></li>
</ul>
</div>


          </div>
        </div>
      </div>
      <div class="sphinxsidebar">
        <div class="sphinxsidebarwrapper">
  <h3><a href="#">Table Of Contents</a></h3>
  <ul>
<li><a class="reference internal" href="#">Bem Vindos ao Circo Voador da Programação Python</a></li>
<li><a class="reference internal" href="#sumario">Sumário</a></li>
<li><a class="reference internal" href="#indices-e-tabelas">Indices e Tabelas</a></li>
</ul>

  <h4>Next topic</h4>
  <p class="topless"><a href="inicia.html"
                        title="next chapter">Primeiro Cenário do Jogo</a></p>
  <h3>This Page</h3>
  <ul class="this-page-menu">
    <li><a href="_sources/index.txt"
           rel="nofollow">Show Source</a></li>
  </ul>
<div id="searchbox" style="display: none">
  <h3>Quick search</h3>
    <form class="search" action="search.html" method="get">
      <input type="text" name="q" />
      <input type="submit" value="Go" />
      <input type="hidden" name="check_keywords" value="yes" />
      <input type="hidden" name="area" value="default" />
    </form>
    <p class="searchtip" style="font-size: 90%">
    Enter search terms or a module, class or function name.
    </p>
</div>
<script type="text/javascript">$('#searchbox').show(0);</script>
        </div>
      </div>
      <div class="clearer"></div>
    </div>
    <div class="related">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="genindex.html" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="inicia.html" title="Primeiro Cenário do Jogo"
             >next</a> |</li>
        <li><a href="#">Flying Circus 0.1.0 documentation</a> &raquo;</li>
      </ul>
    </div>
    <div class="footer">
        &copy; Copyright 2016, Carlo E. T. Oliveira.
      Created using <a href="http://sphinx-doc.org/">Sphinx</a> 1.2.3.
    </div>
'''