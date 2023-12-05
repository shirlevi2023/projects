package src.gameobjects;

import danogl.GameObject;
import danogl.collisions.GameObjectCollection;
import danogl.collisions.Layer;
import danogl.gui.rendering.Renderable;
import danogl.util.Counter;
import danogl.util.Vector2;

/**
 * Display a graphic object on the game window showing as many widgets as lives left.
 */
public class GraphicLifeCounter extends GameObject {
    private final GameObjectCollection gameObjectsCollection;
    private final Counter livesCounter;
    private final GameObject[] levs;

    /**
     * a constructor of the class GraphicLifeCounter
     * @param widgetTopLeftCorner - top left corner of left most life widgets.
     *                           Other widgets will be displayed to its right, aligned in hight.
     * @param widgetDimensions - dimensions of widgets to be displayed.
     * @param livesCounter -  global lives counter of game.
     * @param widgetRenderable -  image to use for widgets.
     * @param gameObjectsCollection - global game object collection managed by game
     *                              manager.
     * @param numOfLives - global setting of number of lives a player will have in a game.
     */
    public GraphicLifeCounter(Vector2 widgetTopLeftCorner,
                              Vector2 widgetDimensions,
                              Counter livesCounter,
                              Renderable widgetRenderable,
                              GameObjectCollection gameObjectsCollection,
                              int numOfLives){
        super(widgetTopLeftCorner, widgetDimensions, widgetRenderable);
        this.gameObjectsCollection = gameObjectsCollection;
        this.livesCounter = livesCounter;
        levs = new GameObject[numOfLives];
        for (int i = 0; i < numOfLives; i++) {
            levs[i] =
                    new GameObject(widgetTopLeftCorner.add(new Vector2(40*i,0)),
                            widgetDimensions, widgetRenderable);


            gameObjectsCollection.addGameObject(levs[i], Layer.BACKGROUND);

        }
    }


    @Override
    public void update(float deltaTime) {
        super.update(deltaTime);
        if (livesCounter.value() >= 0 && livesCounter.value() < 4){
            gameObjectsCollection.removeGameObject(levs[livesCounter.value()],
                    Layer.BACKGROUND);
        }

    }

}
