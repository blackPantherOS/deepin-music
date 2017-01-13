/**
 * Copyright (C) 2016 Deepin Technology Co., Ltd.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 **/

#pragma once

#include <QString>
#include <QMap>
#include "mediameta.h"

class PlaylistMeta
{
public:
    QString uuid;
    QString displayName;
    QString icon;

    int     sortType    = 0;
    bool    editmode    = false;
    bool    readonly    = false;
    bool    hide        = false;
    bool    active      = false;
    bool    unused      = false;

    MetaPtr                  playing;
    QStringList              sortMetas;

    QMap<QString, MetaPtr>   metas;
    QMap<QString, int>       invalidMetas;
};

Q_DECLARE_METATYPE(PlaylistMeta)
