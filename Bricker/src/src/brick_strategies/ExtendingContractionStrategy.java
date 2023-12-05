package src.brick_strategies;

import danogl.GameObject;
import danogl.gui.ImageReader;
import danogl.gui.rendering.Renderable;
import danogl.util.Counter;
import danogl.util.Vector2;
import src.gameobjects.ExtendContract;
import src.gameobjects.Puck;
import src.gameobjects.StatusDefiner;

import java.util.Random;

public class ExtendingContractionStrategy extends RemoveBrickStrategyDecorator {
    private static final Random rand = new Random();
    public static final int FACTOR_SPEED_OF_STATUS_OBJ = 160;
    public static final String BUFF_WIDEN_PNG = "assets/buffWiden.png";
    public static final String BUFF_NARROW_PNG = "assets/buffNarrow.png";
    private final CollisionStrategy toBeDecorated;
    ImageReader imageReader;

    /**
     * a constructor to ExtendingContractionStrategy strategy
     * @param toBeDecorated - a collison strategy to decorated
     * @param imageReader - image reader obj
     */
    ExtendingContractionStrategy(CollisionStrategy toBeDecorated,
                                 ImageReader imageReader) {
        super(toBeDecorated);
        this.imageReader = imageReader;
        this.toBeDecorated = toBeDecorated;
    }

    @Override
    public void onCollision(GameObject thisObj, GameObject otherObj, Counter counter) {
        super.onCollision(thisObj, otherObj, counter);
            Renderable img;
            boolean res = rand.nextBoolean();
            Renderable img1 = imageReader.readImage(BUFF_WIDEN_PNG, true);
            Renderable img2 = imageReader.readImage(BUFF_NARROW_PNG, true);
            if (res){ // extend == true , contract == false

                img = img1;
            }
            else {
                img = img2;
            }
            StatusDefiner statusDefiner = new ExtendContract(thisObj.getCenter(),
                    thisObj.getDimensions(), img, thisObj.getCenter(), res,
                    getGameObjectCollection());
            statusDefiner.setVelocity(new Vector2(0, 1).mult(FACTOR_SPEED_OF_STATUS_OBJ));
            getGameObjectCollection().addGameObject(statusDefiner);

    }


}

