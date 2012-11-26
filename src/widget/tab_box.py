#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Hou Shaohui
# 
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou Shaohui <houshao55@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import gobject
import pango

from dtk.ui.draw import draw_text, draw_pixbuf
from dtk.ui.utils import  alpha_color_hex_to_cairo, container_remove_all, cairo_disable_antialias

from widget.ui_utils import switch_tab
from widget.skin import app_theme
from constant import LIST_WIDTH
 
class Tab(gtk.EventBox):
    __gtype_name__ = "DtkTab"
    
    def __init__(self, title, allocate_widget,  tab_type, index,  total_number, icon=None):
        gtk.EventBox.__init__(self)
        self.set_visible_window(False)
        self.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.unset_flags(gtk.CAN_FOCUS)
        self.connect("set-focus-child", self.on_grab_focus)
        self.connect("grab-focus", self.on_grab_focus)
        self.connect("button-press-event", self.on_tab_button_press)
        self.connect("motion-notify-event", self.on_tab_motion_notify)
        self.connect("button-release-event", self.on_tab_button_release)
        self.connect("enter-notify-event", self.on_tab_enter_notify)
        self.connect("leave-notify-event", self.on_tab_leave_notify)
        self.connect("expose-event", self.on_tab_expose)     
        self.is_in_move= False
        self.press_callback = None
        self.__allocate_widget = allocate_widget
        self.index = index
        self.total = total_number
        self.tab_type = tab_type
        
        # init data.
        self.is_select = False
        self.is_hover = False
        self.title = title 
        self.icon = icon
        self.padding_x = 5
        if self.icon:
            self.icon_pixbuf = gtk.gdk.pixbuf_new_from_file(icon)
            self.icon_size = 16
        else:    
            self.icon_pixbuf =None
            self.icon_size = 0
        
    def on_grab_focus(self, widget, *args):
        if self.press_callback:
            self.press_callback(self)
        self.is_select = True    
        self.queue_draw()
        
    def render(self, cr, rect):    
        color = "#EDF3FA"
        if self.is_select:    
            color = "#FFFFFF"
        alpha_color = (color, 0.95)    
        
        with cairo_disable_antialias(cr):
            cr.set_source_rgba(*alpha_color_hex_to_cairo(alpha_color))
            cr.rectangle(rect.x, rect.y, rect.width, rect.height)
            cr.fill()
            
            cr.set_line_width(1)
            cr.set_source_rgba(*alpha_color_hex_to_cairo(("#D6D6D6", 0.95)))        
            
            if self.index == 0:
                if self.is_select:
                    cr.move_to(rect.x + rect.width, rect.y)
                    cr.rel_line_to(0, rect.height)
                else:    
                    cr.move_to(rect.x, rect.y + rect.height)
                    cr.rel_line_to(rect.width, 0)
                cr.stroke()                                
                    # dashed = [4.0, 4.0]
                    # cr.save()
                    # cr.move_to(rect.x, rect.y + rect.height)
                    # cr.line_to(rect.x + rect.width, rect.y + rect.height)
                    # cr.set_dash(dashed)
                    # cr.stroke()
                    # cr.restore()
            
            elif self.index == self.total - 1:
                if self.is_select:
                    cr.move_to(rect.x + 1, rect.y)
                    cr.rel_line_to(0, rect.height)
                else:    
                    cr.move_to(rect.x, rect.y + rect.height)
                    cr.rel_line_to(rect.width, 0)
                cr.stroke()    
                
            else:    
                if self.is_select:
                    cr.move_to(rect.x + 1, rect.y)
                    cr.rel_line_to(0, rect.height)
                    cr.stroke()
                    
                    cr.save()
                    cr.move_to(rect.x + rect.width, rect.y)
                    cr.rel_line_to(0, rect.height)
                    cr.stroke()
            
                else:    
                    cr.move_to(rect.x, rect.y + rect.height)
                    cr.rel_line_to(rect.width, 0)
                    cr.stroke()
        
        if self.icon_pixbuf:
            icon_y = rect.y + (rect.height - self.icon_size) / 2
            draw_pixbuf(cr, self.icon_pixbuf, rect.x + self.padding_x, rect.y + icon_y)
            
        if self.is_select:    
            color = app_theme.get_color("simpleItemHighlight").get_color()
        elif self.is_hover:    
            color = app_theme.get_color("simpleItemHighlight").get_color()
        else:    
            color = app_theme.get_color("labelText").get_color()
            
        draw_text(cr, self.title, rect.x + self.icon_size + self.padding_x * 2, rect.y, 
                  rect.width - (self.icon_size + self.padding_x * 3), rect.height,
                  text_color= color,
                  alignment=pango.ALIGN_CENTER,
                  text_size=10)
        
        
    def clear_selected_status(self):
        self.is_select = False
        
    def manual_select(self):
        self.is_select = True
        self.queue_draw()
        
    def get_allocate_widget(self):    
        return self.__allocate_widget
        
    def on_tab_expose(self, widget, event):    
        rect = widget.allocation
        cr = widget.window.cairo_create()
        self.render(cr, rect)
        return True
        
    def on_tab_button_press(self, widget, event):    
        self.on_grab_focus(self)
        
    def on_tab_motion_notify(self, widget, event):
        pass
            
    def on_tab_button_release(self, widget, event):
        pass

    def on_tab_enter_notify(self, widget, event):
        self.is_hover = True
        self.queue_draw()
    
    def on_tab_leave_notify(self, widget, event):
        self.is_hover = False
        self.queue_draw()
        
    def close(self, *args):    
        self.destroy()

        
class TabManager(gtk.VBox):        
    __gtype_name__ = 'DtkTabManager'
    __gsignals__ = { 'switch-tab': (gobject.SIGNAL_RUN_LAST, None, (gtk.Widget,)),}
    
    def __init__(self, items, default_height=31):
        gtk.VBox.__init__(self)
        self.set_size_request(LIST_WIDTH, -1)
        
        self.__topbar = gtk.HBox()
        self.__topbar.connect("realize", self.on_topbar_realize)
        self.__topbar.connect("size-allocate", self.on_topbar_size_allocate)
        self.__container = gtk.VBox()
        self.total_number = 0
        
        self.default_height = default_height
        self.items = []
        allocate_align = gtk.Alignment()
        allocate_align.set(1, 1, 1, 1)
        allocate_align.set_padding(0, 0, 0, 0)
        allocate_align.add(self.__container)
        
        self.pack_start(self.__topbar, False, True)
        self.pack_start(allocate_align, True, True)
        
        self.add_items(items)
        
        # Init Status.
        if self.items:
            item = self.items[0]
            item.manual_select()
            self.__container.add(item.get_allocate_widget())
            
    def add_items(self, items, clear=True):        
        if clear:
            self.clear_items()
        self.total_number += len(items)
        for index, (title, allocate_widget, tab_type) in enumerate(items):        
            self.items.append(Tab(title, allocate_widget, tab_type, index, self.total_number))
        self.resize_items()    
            
    def clear_items(self):        
        del self.items[:]
        self.total_number = 0
        
    def repack_items(self):    
        self.resize_item()
            
    def on_topbar_realize(self, widget):   
        self.resize_items(widget)
            
    def resize_items(self, widget=None):        
        if not widget: widget = self.__topbar
        container_remove_all(widget)        
        total = len(self.items)
        if total > 0:
            rect = widget.allocation
            average_width = rect.width / total
            for item in self.items:
                item.press_callback = self.on_item_press
                item.set_size_request(average_width, self.default_height)
                self.__topbar.pack_start(item, False, False)
            widget.show_all()
            
    def on_topbar_size_allocate(self, widget, rect):        
        pass
                
    def on_item_press(self, widget):            
        for item in self.items:
            if item == widget:
                continue
            item.clear_selected_status()
            
        switch_tab(self.__container, widget.get_allocate_widget())    
        self.emit("switch-tab", widget)    
