#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import logging

class Utc(object):
  def __init__(self): 
    pass

  def uct_value(self,total_visit,node_win_score,node_visit):
    if(node_visit == 0):
      return sys.maxint

    utc_score = (node_win_score * 1. / node_visit) + 1.41 * np.sqrt( np.log(total_visit) / node_visit )
    return utc_score


  def find_best_node_utc(self,node):
    parent_visit = node.state.visit_count

    max_score = 0

    max_node = node
    #logging.info("--")
    #logging.info("Level: {}".format(node.level+1))
    for n in node.children:
      score = self.uct_value(parent_visit,n.state.win_score,n.state.visit_count)
      #logging.info("utc score: {}, win_score: {}, visit_count: {}".format(score,n.state.win_score,n.state.visit_count))
      if(score >= max_score):
        max_score = score
        max_node = n

    return max_node