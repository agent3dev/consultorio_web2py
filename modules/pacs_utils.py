#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_next_exp(dc):
    pacs_s = dc.patient.id.max()
    pacs_r = dc().select(pacs_s).first()[pacs_s] or 0
    return pacs_r+1

#print(get_next_exp())
