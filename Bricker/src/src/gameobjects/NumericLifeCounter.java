package src.gameobjects;

import danogl.GameObject;
import danogl.collisions.Layer;
import danogl.gui.rendering.TextRenderable;
import danogl.util.Counter;
import java.awt.*;

/**
 * Display a graphic object on the game window showing a numeric count of lives left.
 */
public class NumericLifeCounter extends GameObject {
    private static final String MSG_OF_REST_HEARTS = "remain: ";
    private final Counter livesCounter;
    TextRenderable textRenderable;

    /**
     * a constructor of the class NumericLifeCounter
     * @param livesCounter -  global lives counter of game.
     * @param topLeftCorner -  top left corner of renderable.
     * @param dimensions - dimensions of renderable.
     * @param gameObjectCollection - global game object collection.
     */

    public NumericLifeCounter(danogl.util.Counter livesCounter,
                              danogl.util.Vector2 topLeftCorner,
                              danogl.util.Vector2 dimensions,
                              danogl.collisions.GameObjectCollection gameObjectCollection){
        super(topLeftCorner, dimensions, null);
        this.livesCounter = livesCounter;
        textRenderable = new TextRenderable(MSG_OF_REST_HEARTS + livesCounter.value());
        textRenderable.setColor(Color.PINK);
        GameObject numericCounter = new GameObject(topLeftCorner, dimensions,
                this.textRenderable);
        gameObjectCollection.addGameObject(numericCounter, Layer.BACKGROUND);
    }

    @Override
    public void update(float deltaTime) {
        super.update(deltaTime);
        this.textRenderable.setString(MSG_OF_REST_HEARTS + this.livesCounter.value());


    }
}
