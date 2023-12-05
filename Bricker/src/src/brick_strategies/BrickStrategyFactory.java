package src.brick_strategies;

import danogl.collisions.GameObjectCollection;
import danogl.gui.ImageReader;
import danogl.gui.SoundReader;
import danogl.gui.UserInputListener;
import danogl.gui.WindowController;
import danogl.util.Vector2;
import src.BrickerGameManager;

import java.util.Random;

/**
 * Factory class for creating Collision strategies
 */
public class BrickStrategyFactory {


    private static final int SPECIAL_BEHAVIORS = 5;
    private static final int NUM_OF_BEHAVIORS = 6;
    private final GameObjectCollection collection;
    private final ImageReader imageReader;
    private final SoundReader soundReader;
    private final UserInputListener inputListener;
    private final Vector2 windowDimensions;
    private final BrickerGameManager gameManager;
    private final WindowController windowController;
    private final Random rand = new Random();

    /**
     * a constructor to BrickStrategyFactory class
     */
    public BrickStrategyFactory(danogl.collisions.GameObjectCollection gameObjectCollection,
                                BrickerGameManager gameManager, danogl.gui.ImageReader imageReader,
                                danogl.gui.SoundReader soundReader, danogl.gui.UserInputListener inputListener,
                                danogl.gui.WindowController windowController,
                                danogl.util.Vector2 windowDimensions){
        this.collection = gameObjectCollection;
        this.imageReader = imageReader;
        this.soundReader = soundReader;
        this.inputListener = inputListener;
        this.windowDimensions = windowDimensions;
        this.gameManager = gameManager;
        this.windowController = windowController;
    }

    /**
     * this func Returns randomly a strategy for brick when its break
     * @return - collision strategy that chosen
     */
    public CollisionStrategy getStrategy() {
        RemoveBrickStrategy defaultBehavior = new RemoveBrickStrategy(collection);
        int idx = rand.nextInt(NUM_OF_BEHAVIORS);

        switch (idx) {
            case 1:
                return new PuckStrategy(defaultBehavior,
                        imageReader, soundReader);
            case 2:
                return new AddPaddleStrategy(defaultBehavior,
                        imageReader, inputListener, windowDimensions);

            case 3:
                return new ChangeCameraStrategy(defaultBehavior, windowController, gameManager);

            case 4:
                return new ExtendingContractionStrategy(defaultBehavior, imageReader);

            case 5:
                return doubleBehavior(defaultBehavior);

            default:
                return defaultBehavior;
        }
    }

    /**
     * this func Returns a double behavior randomly
     * @return - collision strategy that chosen
     */
    private RemoveBrickStrategyDecorator doubleBehavior(CollisionStrategy defaultBehavior){
        int idx = rand.nextInt(SPECIAL_BEHAVIORS);
        switch (idx) {
            case 0:
                return new PuckStrategy(getBehaviorFromSpecials(defaultBehavior),
                        imageReader, soundReader);

            case 1:
                return new AddPaddleStrategy(getBehaviorFromSpecials(defaultBehavior),
                        imageReader, inputListener, windowDimensions);

            case 2:
                return new ChangeCameraStrategy(getBehaviorFromSpecials(defaultBehavior),
                        windowController, gameManager);


            case 3:
                return new ExtendingContractionStrategy(getBehaviorFromSpecials(defaultBehavior), imageReader);

            case 4:
                return getBehaviorFromSpecials(getBehaviorFromSpecials(getBehaviorFromSpecials(defaultBehavior)));

            default:
                return null;
        }

    }

    /**
     * this func Returns randomly a strategy for brick when its break - from specials
     * strategies
     * @return - collision strategy that chosen
     */
    private RemoveBrickStrategyDecorator getBehaviorFromSpecials(CollisionStrategy defaultBehavior) {
        int idx = rand.nextInt(SPECIAL_BEHAVIORS - 1); // rand from 4 behaviors
        switch (idx) {
            case 0:
                return new PuckStrategy(defaultBehavior,
                        imageReader, soundReader);


            case 1:
                return new AddPaddleStrategy(defaultBehavior,
                        imageReader, inputListener, windowDimensions);

            case 2:
                return new ChangeCameraStrategy(defaultBehavior, windowController, gameManager);


            case 3:
                return new ExtendingContractionStrategy(defaultBehavior, imageReader);

            default:
                return null;
        }

        }


}
