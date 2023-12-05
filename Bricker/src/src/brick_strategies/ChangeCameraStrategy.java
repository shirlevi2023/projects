package src.brick_strategies;

import danogl.GameObject;
import danogl.collisions.Layer;
import danogl.gui.WindowController;
import danogl.gui.rendering.Camera;
import danogl.util.Counter;
import danogl.util.Vector2;
import src.BrickerGameManager;
import src.gameobjects.Ball;
import src.gameobjects.BallCollisionCountdownAgent;
import src.gameobjects.Puck;

/**
 * Concrete class extending abstract RemoveBrickStrategyDecorator.
 * Changes camera focus from ground to ball until ball collides
 * NUM_BALL_COLLISIONS_TO_TURN_OFF times.
 */
public class ChangeCameraStrategy extends RemoveBrickStrategyDecorator {
    private static final int COLLISIONS_TO_RESET_CAMERA = 4;
    private final BrickerGameManager gameManager;
    private final WindowController windowController;
    private Ball ball;
    private static boolean isNotLocked;
    BallCollisionCountdownAgent agent;

    /**
     * a constructor to ChangeCameraStrategy.
     */
    ChangeCameraStrategy(CollisionStrategy toBeDecorated,
                         danogl.gui.WindowController windowController
            , BrickerGameManager gameManager) {
        super(toBeDecorated);
        isNotLocked = true;
        this.gameManager = gameManager;
        this.windowController = windowController;
    }

    @Override
    public void onCollision(GameObject thisObj, GameObject otherObj, Counter counter) {
        super.onCollision(thisObj, otherObj, counter);
        for (GameObject obj : getGameObjectCollection()) {
            if (obj instanceof Ball && !(obj instanceof Puck)) {
                ball = (Ball) obj;
                break;
            }
        }
        if (isNotLocked) {
            isNotLocked = false;
            gameManager.setCamera(
                    new Camera(
                            ball,            //object to follow
                            Vector2.ZERO,    //follow the center of the object
                            windowController.getWindowDimensions().mult(1.2f),  //widen the frame a bit
                            windowController.getWindowDimensions()   //share the window dimensions
                    )
            );
            agent = new BallCollisionCountdownAgent(ball, this,
                    COLLISIONS_TO_RESET_CAMERA);
            getGameObjectCollection().addGameObject(agent, Layer.BACKGROUND);
        }
    }

    /**
     * Return camera to normal ground position.
     */
    public void turnOffCameraChange() {
        gameManager.setCamera(null);
        isNotLocked = true;
        getGameObjectCollection().removeGameObject(agent, Layer.BACKGROUND);
    }
}
