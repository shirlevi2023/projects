package src.brick_strategies;

import danogl.GameObject;

import danogl.gui.ImageReader;
import danogl.gui.Sound;
import danogl.gui.SoundReader;
import danogl.gui.rendering.Renderable;
import danogl.util.Counter;
import danogl.util.Vector2;
import src.gameobjects.Puck;

/**
 * Concrete class extending abstract RemoveBrickStrategyDecorator.
 * Introduces several pucks instead of brick once removed.
 */
public class PuckStrategy extends RemoveBrickStrategyDecorator {
    public static final String MOCK_BALL_PNG = "assets/mockBall.png";
    public static final String BLOP_CUT_SILENCED_WAV = "assets/blop_cut_silenced.wav";
    public static final int NUM_OF_PUCKS = 3;
    public static final int FACTOR_PUCK_SIZE = 3;
    public static final int PUCKS_SPEED = 160;
    CollisionStrategy toBeDecorated;
    ImageReader imageReader;
    SoundReader soundReader;

    /**
     * a constructor for the puck strategy
     */
    public PuckStrategy(CollisionStrategy toBeDecorated,
                         danogl.gui.ImageReader imageReader,
                         danogl.gui.SoundReader soundReader){
        super(toBeDecorated);
        this.toBeDecorated = toBeDecorated;
        this.imageReader = imageReader;
        this.soundReader = soundReader;
    }

    @Override
    public void onCollision(GameObject thisObj, GameObject otherObj, Counter counter) {
        super.onCollision(thisObj, otherObj, counter);
        int[][] directions = {{1,1}, {0,1}, {-1,1}};
        float puckSize = (thisObj.getDimensions().x() / FACTOR_PUCK_SIZE);
        Renderable puckImage = imageReader.readImage(MOCK_BALL_PNG, true);
        Sound collisionSound = soundReader.readSound(BLOP_CUT_SILENCED_WAV);
        for (int i = 0; i < NUM_OF_PUCKS; i++) {
            Puck puck = new Puck(
                    new Vector2(thisObj.getCenter().x()- (puckSize / 2),
                    thisObj.getCenter().y()),
                    new Vector2(puckSize, puckSize), puckImage, collisionSound);
            getGameObjectCollection().addGameObject(puck);
            puck.setVelocity(new Vector2(directions[i][0], directions[i][1]).mult(PUCKS_SPEED));


        }
    }
}
