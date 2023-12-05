package src.brick_strategies;

import danogl.GameObject;
import danogl.gui.ImageReader;
import danogl.gui.UserInputListener;
import danogl.gui.rendering.Renderable;
import danogl.util.Counter;
import danogl.util.Vector2;
import src.gameobjects.MockPaddle;

/**
 * Concrete class extending abstract RemoveBrickStrategyDecorator. Introduces extra paddle to game window which remains until colliding
 * NUM_COLLISIONS_FOR_MOCK_PADDLE_DISAPPEARANCE with other game objects.
 */
public class AddPaddleStrategy extends RemoveBrickStrategyDecorator {
    private static final String PADDLE_PATH = "assets/paddle.png";
    private static final float PADDLE_SIZE_X = 100;
    private static final float PADDLE_SIZE_Y = 15;
    public static final int NUM_COLLISIONS_TO_DISAPPEAR = 3;
    private final UserInputListener inputListener;
    private final ImageReader imageReader;
    private final Vector2 windowDimensions;
    private static final int minDistanceFromEdge = 25;
    private final CollisionStrategy toBeDecorated;

    /**
     * a constructor to AddPaddleStrategy class
     */
    AddPaddleStrategy(CollisionStrategy toBeDecorated,
                      danogl.gui.ImageReader imageReader,
                      danogl.gui.UserInputListener inputListener,
                      danogl.util.Vector2 windowDimensions){
        super(toBeDecorated);
        this.toBeDecorated = toBeDecorated;
        this.imageReader = imageReader;
        this.inputListener = inputListener;
        this.windowDimensions =  windowDimensions;


    }

    @Override
    public void onCollision(GameObject thisObj, GameObject otherObj, Counter counter) {
        super.onCollision(thisObj, otherObj, counter);
        if (!(MockPaddle.isInstantiated)){
            Renderable paddleImage = imageReader.readImage(PADDLE_PATH, true);
            MockPaddle mockpaddle = new MockPaddle(Vector2.ZERO, new Vector2(PADDLE_SIZE_X,
                    PADDLE_SIZE_Y), paddleImage, inputListener, windowDimensions,
                    getGameObjectCollection(), minDistanceFromEdge, NUM_COLLISIONS_TO_DISAPPEAR);
            mockpaddle.setCenter(new Vector2(windowDimensions.x()/ 2,
                    windowDimensions.y()/2));
            toBeDecorated.getGameObjectCollection().addGameObject(mockpaddle);

        }


    }
}
