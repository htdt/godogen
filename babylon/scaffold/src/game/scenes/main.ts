import type { BabylonApp } from "../../app/BabylonApp";
import {
  ArcRotateCamera,
  Color3,
  CreateBox,
  CreateGround,
  HemisphericLight,
  Scene,
  StandardMaterial,
  Vector3
} from "../../app/babylon";

export async function createScene(app: BabylonApp): Promise<Scene> {
  const scene = new Scene(app.engine);

  scene.clearColor.set(0.04, 0.04, 0.06, 1);

  const camera = new ArcRotateCamera(
    "camera",
    Math.PI / 4,
    Math.PI / 3,
    12,
    Vector3.Zero(),
    scene
  );
  camera.attachControl(app.canvas, true);

  const light = new HemisphericLight("light", new Vector3(0, 1, 0), scene);
  light.intensity = 0.9;

  const ground = CreateGround("ground", { width: 12, height: 12 }, scene);
  const groundMaterial = new StandardMaterial("ground-material", scene);
  groundMaterial.diffuseColor = new Color3(0.24, 0.28, 0.24);
  ground.material = groundMaterial;

  const marker = CreateBox("marker", { size: 1.2 }, scene);
  marker.position.y = 0.6;
  const markerMaterial = new StandardMaterial("marker-material", scene);
  markerMaterial.diffuseColor = new Color3(0.95, 0.6, 0.25);
  marker.material = markerMaterial;

  scene.onBeforeRenderObservable.add(() => {
    const delta = scene.getEngine().getDeltaTime() / 1000;
    marker.rotation.y += delta;
  });

  return scene;
}
