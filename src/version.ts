// *****************************************************************************
//
//   Part of the py5jupyter (& py5) library
//   Copyright (C) 2022-2024 Jim Schmitz
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

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = require('../package.json');

/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
export const MODULE_VERSION = data.version;

/*
 * The current package name.
 */
export const MODULE_NAME = data.name;
