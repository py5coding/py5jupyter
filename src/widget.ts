// *****************************************************************************
//
//   Part of the py5jupyter (& py5) library
//   Copyright (C) 2022 Jim Schmitz
//
//   This library is free software: you can redistribute it and/or modify it
//   under the terms of the GNU Lesser General Public License as published by
//   the Free Software Foundation, either version 2.1 of the License, or (at
//   your option) any later version.
//
//   This library is distributed in the hope that it will be useful, but
//   WITHOUT ANY WARRANTY; without even the implied warranty of
//   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
//   General Public License for more details.
//
//   You should have received a copy of the GNU Lesser General Public License
//   along with this library. If not, see <https://www.gnu.org/licenses/>.
//
// *****************************************************************************
import {
  DOMWidgetModel,
  DOMWidgetView,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';


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
  private _img: HTMLImageElement;
  private _canvas: HTMLCanvasElement;
  private _ctx: CanvasRenderingContext2D;

  render() {
    this._img = document.createElement('img');
    this._img.width = this.model.get('width');
    this._img.height = this.model.get('height');

    this._canvas = document.createElement('canvas');
    this._canvas.width = this.model.get('width');
    this._canvas.height = this.model.get('height');
    this._canvas.tabIndex = 0;

    const ctx = this._canvas.getContext('2d');
    if (ctx === null) {
      throw 'Could not create 2d context.';
    } else {
      this._ctx = ctx;
    }

    this._updateImgSrc();
    this._ctx.drawImage(this._img, 0, 0);
    this.el.appendChild(this._canvas);

    this._canvas.addEventListener('keydown', {
      handleEvent: this.onKeyDown.bind(this)
    });
    this._canvas.addEventListener('keypress', {
      handleEvent: this.onKeyPress.bind(this)
    });
    this._canvas.addEventListener('keyup', {
      handleEvent: this.onKeyUp.bind(this)
    });
    this._canvas.addEventListener('mouseenter', {
      handleEvent: this.onMouseEnter.bind(this)
    });
    this._canvas.addEventListener('mousedown', {
      handleEvent: this.onMouseDown.bind(this)
    });
    this._canvas.addEventListener('mousemove', {
      handleEvent: this.onMouseMove.bind(this)
    });
    this._canvas.addEventListener('mouseup', {
      handleEvent: this.onMouseUp.bind(this)
    });
    this._canvas.addEventListener('mouseleave', {
      handleEvent: this.onMouseLeave.bind(this)
    });
    this._canvas.addEventListener('click', {
      handleEvent: this.onMouseClick.bind(this)
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
    this._img.src = url;
    this._ctx.drawImage(this._img, 0, 0);
  }

  // https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent

  private onKeyDown(event: KeyboardEvent) {
    this.model.send({ event: 'key_down', key: event.key, repeat: event.repeat, ...this.getModifiers(event) }, {});
  }

  private onKeyPress(event: KeyboardEvent) {
    this.model.send({ event: 'key_press', key: event.key, repeat: event.repeat, ...this.getModifiers(event) }, {});
  }

  private onKeyUp(event: KeyboardEvent) {
    this.model.send({ event: 'key_up', key: event.key, repeat: event.repeat, ...this.getModifiers(event) }, {});
  }

  private onMouseEnter(event: MouseEvent) {
    this.model.send({ event: 'mouse_enter', buttons: event.buttons, ...this.getModifiers(event), ...this.getCoordinates(event) }, {});
  }

  private onMouseDown(event: MouseEvent) {
    // Bring focus to the img element, so keyboard events can be triggered
    this._canvas.focus();

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

  private onMouseClick(event: MouseEvent) {
    this.model.send({ event: 'mouse_click', buttons: event.buttons, ...this.getModifiers(event), ...this.getCoordinates(event) }, {});
  }

  protected getCoordinates(event: MouseEvent | Touch) {
    // https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent
    const rect = this._canvas.getBoundingClientRect();

    const x = (this._canvas.width * (event.clientX - rect.left)) / rect.width;
    const y = (this._canvas.height * (event.clientY - rect.top)) / rect.height;

    return { x, y };
  }

  protected getModifiers(event: MouseEvent | KeyboardEvent) {
    return {mod: (+event.shiftKey) * 1 + (+event.ctrlKey) * 2 + (+event.metaKey) * 4 + (+event.altKey) * 8};
  }

}
