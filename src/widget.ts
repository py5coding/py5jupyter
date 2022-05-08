// Copyright (c) Jim Schmitz
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

export class ExampleModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: ExampleModel.model_name,
      _model_module: ExampleModel.model_module,
      _model_module_version: ExampleModel.model_module_version,
      _view_name: ExampleModel.view_name,
      _view_module: ExampleModel.view_module,
      _view_module_version: ExampleModel.view_module_version,
      value: 'Hello World',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'ExampleModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ExampleView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

export class ExampleView extends DOMWidgetView {
  render() {
    this.el.classList.add('custom-widget');

    this.value_changed();
    this.model.on('change:value', this.value_changed, this);
  }

  value_changed() {
    this.el.textContent = this.model.get('value');
  }
}


export class Py5SketchPortalModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: Py5SketchPortalModel.model_name,
      _model_module: Py5SketchPortalModel.model_module,
      _model_module_version: Py5SketchPortalModel.model_module_version,
      _view_name: Py5SketchPortalModel.view_name,
      _view_module: Py5SketchPortalModel.view_module,
      _view_module_version: Py5SketchPortalModel.view_module_version,
      format: 'jpeg',
      width: '',
      height: '',
      value: new DataView(new ArrayBuffer(0)),
    };
  }

  static serializers = {
    ...DOMWidgetModel.serializers,
    value: {
      serialize: (value: any): DataView => {
        return new DataView(value.buffer.slice(0));
      },
    },
  };

  static model_name = 'Py5SketchPortalModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'Py5SketchPortalView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

export class Py5SketchPortalView extends DOMWidgetView {
  private _imgEl: HTMLImageElement;

  render() {
    this._imgEl = document.createElement('img');
    this._imgEl.tabIndex = 0;
    this._updateImgSrc();
    this.el.appendChild(this._imgEl);

    this._imgEl.addEventListener('keydown', {
      handleEvent: this.onKeyDown.bind(this)
    });
    this._imgEl.addEventListener('keypress', {
      handleEvent: this.onKeyPress.bind(this)
    });
    this._imgEl.addEventListener('keyup', {
      handleEvent: this.onKeyUp.bind(this)
    });
    this._imgEl.addEventListener('mouseenter', {
      handleEvent: this.onMouseEnter.bind(this)
    });
    this._imgEl.addEventListener('mousedown', {
      handleEvent: this.onMouseDown.bind(this)
    });
    this._imgEl.addEventListener('mousemove', {
      handleEvent: this.onMouseMove.bind(this)
    });
    this._imgEl.addEventListener('mouseup', {
      handleEvent: this.onMouseUp.bind(this)
    });
    this._imgEl.addEventListener('mouseleave', {
      handleEvent: this.onMouseLeave.bind(this)
    });

    // Python -> JavaScript update
    this.model.on('change:value', this._updateImgSrc, this);
  }

  private _updateImgSrc() {
    const value = this.model.get('value');
    const blob = new Blob([value], {
      type: `image/${this.model.get('format')}`,
    });
    const url = URL.createObjectURL(blob);
    this._imgEl.src = url;
  }

  // https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent

  private onKeyDown(event: KeyboardEvent) {
    this.model.send({ event: 'key_down', key: event.key, ...this.getModifiers(event) }, {});
  }

  private onKeyPress(event: KeyboardEvent) {
    this.model.send({ event: 'key_press', key: event.key, ...this.getModifiers(event) }, {});
  }

  private onKeyUp(event: KeyboardEvent) {
    this.model.send({ event: 'key_up', key: event.key, ...this.getModifiers(event) }, {});
  }

  private onMouseEnter(event: MouseEvent) {
    this.model.send({ event: 'mouse_enter', buttons: event.buttons, ...this.getModifiers(event), ...this.getCoordinates(event) }, {});
  }

  private onMouseDown(event: MouseEvent) {
    // Bring focus to the img element, so keyboard events can be triggered
    this._imgEl.focus();

    this.model.send({ event: 'mouse_down', buttons: event.buttons, ...this.getModifiers(event), ...this.getCoordinates(event) }, {});
  }

  // https://developer.mozilla.org/en-US/docs/Web/API/GlobalEventHandlers
  private onMouseMove(event: MouseEvent) {
    this.model.send({ event: 'mouse_move', buttons: event.buttons, ...this.getModifiers(event), ...this.getCoordinates(event) }, {});
  }

  private onMouseUp(event: MouseEvent) {
    this.model.send({ event: 'mouse_up', buttons: event.buttons, ...this.getModifiers(event), ...this.getCoordinates(event) }, {});
  }

  private onMouseLeave(event: MouseEvent) {
    this.model.send({ event: 'mouse_leave', buttons: event.buttons, ...this.getModifiers(event), ...this.getCoordinates(event) }, {});
  }

  protected getCoordinates(event: MouseEvent | Touch) {
    // https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent
    const rect = this._imgEl.getBoundingClientRect();

    const x = (this._imgEl.width * (event.clientX - rect.left)) / rect.width;
    const y = (this._imgEl.height * (event.clientY - rect.top)) / rect.height;

    return { x, y };
  }

  protected getModifiers(event: MouseEvent | KeyboardEvent) {
    return {mod: (+event.shiftKey) * 1 + (+event.ctrlKey) * 2 + (+event.metaKey) * 4 + (+event.altKey) * 8};
  }

}
