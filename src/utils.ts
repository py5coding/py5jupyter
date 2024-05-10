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

// The below function came from the wonderful Python library ipycanvas
// https://github.com/martinRenou/ipycanvas

export async function bufferToImage(buffer: any): Promise<HTMLImageElement> {
    let url: string;

    const blob = new Blob([buffer], { type: 'image/jpeg' });
    url = URL.createObjectURL(blob);

    const img = new Image();
    return new Promise(resolve => {
        img.onload = () => {
            resolve(img);
        };
        img.src = url;
    });
}
