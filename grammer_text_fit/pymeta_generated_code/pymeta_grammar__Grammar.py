def createParserClass(GrammarBase, ruleGlobals):
    if ruleGlobals is None:
        ruleGlobals = {}
    class Grammar(GrammarBase):
        def rule_text(self):
            _locals = {'self': self}
            self.locals['text'] = _locals
            def _G_many1_1():
                self._trace(' \n    sentence', (51, 65), self.input.position)
                _G_apply_2, lastError = self._apply(self.rule_sentence, "sentence", [])
                self.considerError(lastError, None)
                return (_G_apply_2, self.currentError)
            _G_many1_3, lastError = self.many(_G_many1_1, _G_many1_1())
            self.considerError(lastError, 'text')
            _locals['d'] = _G_many1_3
            _G_python_5, lastError = eval(self._G_expr_4, self.globals, _locals), None
            self.considerError(lastError, 'text')
            return (_G_python_5, self.currentError)


        def rule_sentence(self):
            _locals = {'self': self}
            self.locals['sentence'] = _locals
            def _G_or_6():
                self._trace('\n    differential_sentence', (97, 123), self.input.position)
                _G_apply_7, lastError = self._apply(self.rule_differential_sentence, "differential_sentence", [])
                self.considerError(lastError, None)
                _locals['d'] = _G_apply_7
                self._trace('  punct', (125, 132), self.input.position)
                _G_apply_8, lastError = self._apply(self.rule_punct, "punct", [])
                self.considerError(lastError, None)
                _locals['p'] = _G_apply_8
                _G_python_9, lastError = eval(self._G_expr_4, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_9, self.currentError)
            def _G_or_10():
                self._trace('   unmarked_token', (151, 168), self.input.position)
                _G_apply_11, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_11
                self._trace('            punct', (170, 187), self.input.position)
                _G_apply_12, lastError = self._apply(self.rule_punct, "punct", [])
                self.considerError(lastError, None)
                _locals['p'] = _G_apply_12
                _G_python_14, lastError = eval(self._G_expr_13, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_14, self.currentError)
            _G_or_15, lastError = self._or([_G_or_6, _G_or_10])
            self.considerError(lastError, 'sentence')
            return (_G_or_15, self.currentError)


        def rule_differential_sentence(self):
            _locals = {'self': self}
            self.locals['differential_sentence'] = _locals
            def _G_lookahead_16():
                self._trace('expanded_text', (362, 375), self.input.position)
                _G_apply_17, lastError = self._apply(self.rule_expanded_text, "expanded_text", [])
                self.considerError(lastError, None)
                _locals['search_in'] = _G_apply_17
                return (_G_apply_17, self.currentError)
            _G_lookahead_18, lastError = self.lookahead(_G_lookahead_16)
            self.considerError(lastError, 'differential_sentence')
            self._trace("                        # obtain tokens with expansions\n    difference_in(search_in['difference'])", (386, 484), self.input.position)
            _G_python_20, lastError = eval(self._G_expr_19, self.globals, _locals), None
            self.considerError(lastError, 'differential_sentence')
            _G_apply_21, lastError = self._apply(self.rule_difference_in, "difference_in", [_G_python_20])
            self.considerError(lastError, 'differential_sentence')
            _locals['d'] = _G_apply_21
            self._trace('           # compute the difference \n    take_all', (486, 535), self.input.position)
            _G_apply_22, lastError = self._apply(self.rule_take_all, "take_all", [])
            self.considerError(lastError, 'differential_sentence')
            _G_python_24, lastError = eval(self._G_expr_23, self.globals, _locals), None
            self.considerError(lastError, 'differential_sentence')
            return (_G_python_24, self.currentError)


        def rule_expanded_text(self):
            _locals = {'self': self}
            self.locals['expanded_text'] = _locals
            def _G_or_25():
                def _G_many1_26():
                    self._trace('\n    expansion', (728, 742), self.input.position)
                    _G_apply_27, lastError = self._apply(self.rule_expansion, "expansion", [])
                    self.considerError(lastError, None)
                    return (_G_apply_27, self.currentError)
                _G_many1_28, lastError = self.many(_G_many1_26, _G_many1_26())
                self.considerError(lastError, None)
                _locals['yet_parsed'] = _G_many1_28
                _G_python_30, lastError = eval(self._G_expr_29, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_30, self.currentError)
            def _G_or_31():
                self._trace('   invisible_tokens', (813, 832), self.input.position)
                _G_apply_32, lastError = self._apply(self.rule_invisible_tokens, "invisible_tokens", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_32
                _G_python_34, lastError = eval(self._G_expr_33, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_34, self.currentError)
            _G_or_35, lastError = self._or([_G_or_25, _G_or_31])
            self.considerError(lastError, 'expanded_text')
            return (_G_or_35, self.currentError)


        def rule_expansion(self):
            _locals = {'self': self}
            self.locals['expansion'] = _locals
            def _G_or_36():
                self._trace('\n        except_S', (910, 927), self.input.position)
                _G_apply_37, lastError = self._apply(self.rule_except_S, "except_S", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_37
                _G_python_38, lastError = eval(self._G_expr_13, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_38, self.currentError)
            def _G_or_39():
                self._trace('   in_while_S_A_C', (947, 964), self.input.position)
                _G_apply_40, lastError = self._apply(self.rule_in_while_S_A_C, "in_while_S_A_C", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_40
                _G_python_41, lastError = eval(self._G_expr_13, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_41, self.currentError)
            def _G_or_42():
                self._trace('   the_same_A_as_S', (978, 996), self.input.position)
                _G_apply_43, lastError = self._apply(self.rule_the_same_A_as_S, "the_same_A_as_S", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_43
                _G_python_44, lastError = eval(self._G_expr_13, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_44, self.currentError)
            def _G_or_45():
                self._trace('   P_than_S', (1009, 1020), self.input.position)
                _G_apply_46, lastError = self._apply(self.rule_P_than_S, "P_than_S", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_46
                _G_python_47, lastError = eval(self._G_expr_13, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_47, self.currentError)
            def _G_or_48():
                self._trace('   X_other_hand_X', (1040, 1057), self.input.position)
                _G_apply_49, lastError = self._apply(self.rule_X_other_hand_X, "X_other_hand_X", [])
                self.considerError(lastError, None)
                _locals['x'] = _G_apply_49
                _G_python_50, lastError = eval(self._G_expr_13, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_50, self.currentError)
            _G_or_51, lastError = self._or([_G_or_36, _G_or_39, _G_or_42, _G_or_45, _G_or_48])
            self.considerError(lastError, 'expansion')
            return (_G_or_51, self.currentError)


        def rule_in_while_S_A_C(self):
            _locals = {'self': self}
            self.locals['in_while_S_A_C'] = _locals
            def _G_consumedby_52():
                def _G_many_53():
                    self._trace('unmarked_token', (1122, 1136), self.input.position)
                    _G_apply_54, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                    self.considerError(lastError, None)
                    return (_G_apply_54, self.currentError)
                _G_many_55, lastError = self.many(_G_many_53)
                self.considerError(lastError, None)
                return (_G_many_55, self.currentError)
            _G_consumedby_56, lastError = self.consumedby(_G_consumedby_52)
            self.considerError(lastError, 'in_while_S_A_C')
            _locals['a1'] = _G_consumedby_56
            self._trace(' in_while', (1141, 1150), self.input.position)
            _G_apply_57, lastError = self._apply(self.rule_in_while, "in_while", [])
            self.considerError(lastError, 'in_while_S_A_C')
            _locals['x'] = _G_apply_57
            def _G_consumedby_58():
                def _G_many_59():
                    self._trace('unmarked_token', (1154, 1168), self.input.position)
                    _G_apply_60, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                    self.considerError(lastError, None)
                    return (_G_apply_60, self.currentError)
                _G_many_61, lastError = self.many(_G_many_59)
                self.considerError(lastError, None)
                return (_G_many_61, self.currentError)
            _G_consumedby_62, lastError = self.consumedby(_G_consumedby_58)
            self.considerError(lastError, 'in_while_S_A_C')
            _locals['a2'] = _G_consumedby_62
            _G_python_64, lastError = eval(self._G_expr_63, self.globals, _locals), None
            self.considerError(lastError, 'in_while_S_A_C')
            return (_G_python_64, self.currentError)


        def rule_in_while(self):
            _locals = {'self': self}
            self.locals['in_while'] = _locals
            self._trace('_while = \n ', (1206, 1217), self.input.position)
            _G_apply_65, lastError = self._apply(self.rule_while, "while", [])
            self.considerError(lastError, 'in_while')
            _locals['m'] = _G_apply_65
            _G_python_67, lastError = eval(self._G_expr_66, self.globals, _locals), None
            self.considerError(lastError, 'in_while')
            _locals['l'] = _G_python_67
            self._trace('se(m)):l\n   ', (1268, 1280), self.input.position)
            _G_python_69, lastError = eval(self._G_expr_68, self.globals, _locals), None
            self.considerError(lastError, 'in_while')
            _G_apply_70, lastError = self._apply(self.rule_take, "take", [_G_python_69])
            self.considerError(lastError, 'in_while')
            _locals['search_in'] = _G_apply_70
            self._trace('earch_in\n    difference_in(se', (1290, 1319), self.input.position)
            _G_python_72, lastError = eval(self._G_expr_71, self.globals, _locals), None
            self.considerError(lastError, 'in_while')
            _G_apply_73, lastError = self._apply(self.rule_difference_in, "difference_in", [_G_python_72])
            self.considerError(lastError, 'in_while')
            _locals['d'] = _G_apply_73
            _G_python_75, lastError = eval(self._G_expr_74, self.globals, _locals), None
            self.considerError(lastError, 'in_while')
            return (_G_python_75, self.currentError)


        def rule_except_S(self):
            _locals = {'self': self}
            self.locals['except_S'] = _locals
            def _G_consumedby_76():
                def _G_many_77():
                    self._trace('cept_S = \n    ', (1402, 1416), self.input.position)
                    _G_apply_78, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                    self.considerError(lastError, None)
                    return (_G_apply_78, self.currentError)
                _G_many_79, lastError = self.many(_G_many_77)
                self.considerError(lastError, None)
                return (_G_many_79, self.currentError)
            _G_consumedby_80, lastError = self.consumedby(_G_consumedby_76)
            self.considerError(lastError, 'except_S')
            _locals['a1'] = _G_consumedby_80
            self._trace('rked_to', (1421, 1428), self.input.position)
            _G_apply_81, lastError = self._apply(self.rule_except, "except", [])
            self.considerError(lastError, 'except_S')
            _locals['m'] = _G_apply_81
            self._trace('n*>:a1 e', (1430, 1438), self.input.position)
            _G_apply_82, lastError = self._apply(self.rule_subject, "subject", [])
            self.considerError(lastError, 'except_S')
            _locals['x'] = _G_apply_82
            def _G_consumedby_83():
                def _G_many_84():
                    self._trace('t:m subject:x ', (1442, 1456), self.input.position)
                    _G_apply_85, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                    self.considerError(lastError, None)
                    return (_G_apply_85, self.currentError)
                _G_many_86, lastError = self.many(_G_many_84)
                self.considerError(lastError, None)
                return (_G_many_86, self.currentError)
            _G_consumedby_87, lastError = self.consumedby(_G_consumedby_83)
            self.considerError(lastError, 'except_S')
            _locals['a2'] = _G_consumedby_87
            _G_python_89, lastError = eval(self._G_expr_88, self.globals, _locals), None
            self.considerError(lastError, 'except_S')
            return (_G_python_89, self.currentError)


        def rule_the_same_A_as_S(self):
            _locals = {'self': self}
            self.locals['the_same_A_as_S'] = _locals
            def _G_consumedby_90():
                def _G_many_91():
                    self._trace('_as_S =\n    (<', (1564, 1578), self.input.position)
                    _G_apply_92, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                    self.considerError(lastError, None)
                    return (_G_apply_92, self.currentError)
                _G_many_93, lastError = self.many(_G_many_91)
                self.considerError(lastError, None)
                return (_G_many_93, self.currentError)
            _G_consumedby_94, lastError = self.consumedby(_G_consumedby_90)
            self.considerError(lastError, 'the_same_A_as_S')
            _locals['a1'] = _G_consumedby_94
            self._trace('ed_token*', (1585, 1594), self.input.position)
            _G_apply_95, lastError = self._apply(self.rule_the_same, "the_same", [])
            self.considerError(lastError, 'the_same_A_as_S')
            _locals['m'] = _G_apply_95
            self._trace('):a1 th', (1596, 1603), self.input.position)
            _G_apply_96, lastError = self._apply(self.rule_aspect, "aspect", [])
            self.considerError(lastError, 'the_same_A_as_S')
            _locals['a'] = _G_apply_96
            self._trace('sam', (1605, 1608), self.input.position)
            _G_apply_97, lastError = self._apply(self.rule_as, "as", [])
            self.considerError(lastError, 'the_same_A_as_S')
            self._trace('e:m aspe', (1608, 1616), self.input.position)
            _G_apply_98, lastError = self._apply(self.rule_subject, "subject", [])
            self.considerError(lastError, 'the_same_A_as_S')
            _locals['s'] = _G_apply_98
            def _G_consumedby_99():
                def _G_many_100():
                    self._trace(' as subject:s ', (1620, 1634), self.input.position)
                    _G_apply_101, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                    self.considerError(lastError, None)
                    return (_G_apply_101, self.currentError)
                _G_many_102, lastError = self.many(_G_many_100)
                self.considerError(lastError, None)
                return (_G_many_102, self.currentError)
            _G_consumedby_103, lastError = self.consumedby(_G_consumedby_99)
            self.considerError(lastError, 'the_same_A_as_S')
            _locals['a2'] = _G_consumedby_103
            _G_python_105, lastError = eval(self._G_expr_104, self.globals, _locals), None
            self.considerError(lastError, 'the_same_A_as_S')
            return (_G_python_105, self.currentError)


        def rule_P_than_S(self):
            _locals = {'self': self}
            self.locals['P_than_S'] = _locals
            def _G_consumedby_106():
                def _G_many_107():
                    self._trace('     \nP_than_S', (1735, 1749), self.input.position)
                    _G_apply_108, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                    self.considerError(lastError, None)
                    return (_G_apply_108, self.currentError)
                _G_many_109, lastError = self.many(_G_many_107)
                self.considerError(lastError, None)
                return (_G_many_109, self.currentError)
            _G_consumedby_110, lastError = self.consumedby(_G_consumedby_106)
            self.considerError(lastError, 'P_than_S')
            _locals['a1'] = _G_consumedby_110
            self._trace('   <u', (1754, 1759), self.input.position)
            _G_apply_111, lastError = self._apply(self.rule_than, "than", [])
            self.considerError(lastError, 'P_than_S')
            _locals['m'] = _G_apply_111
            self._trace('arked_to', (1761, 1769), self.input.position)
            _G_apply_112, lastError = self._apply(self.rule_subject, "subject", [])
            self.considerError(lastError, 'P_than_S')
            _locals['x'] = _G_apply_112
            def _G_consumedby_113():
                def _G_many_114():
                    self._trace('>:a1 than:m su', (1773, 1787), self.input.position)
                    _G_apply_115, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                    self.considerError(lastError, None)
                    return (_G_apply_115, self.currentError)
                _G_many_116, lastError = self.many(_G_many_114)
                self.considerError(lastError, None)
                return (_G_many_116, self.currentError)
            _G_consumedby_117, lastError = self.consumedby(_G_consumedby_113)
            self.considerError(lastError, 'P_than_S')
            _locals['a2'] = _G_consumedby_117
            _G_python_118, lastError = eval(self._G_expr_88, self.globals, _locals), None
            self.considerError(lastError, 'P_than_S')
            return (_G_python_118, self.currentError)


        def rule_X_other_hand_X(self):
            _locals = {'self': self}
            self.locals['X_other_hand_X'] = _locals
            def _G_consumedby_119():
                def _G_many_120():
                    self._trace('        \nX_oth', (1893, 1907), self.input.position)
                    _G_apply_121, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                    self.considerError(lastError, None)
                    return (_G_apply_121, self.currentError)
                _G_many_122, lastError = self.many(_G_many_120)
                self.considerError(lastError, None)
                return (_G_many_122, self.currentError)
            _G_consumedby_123, lastError = self.consumedby(_G_consumedby_119)
            self.considerError(lastError, 'X_other_hand_X')
            _locals['a1'] = _G_consumedby_123
            self._trace('nd_X = \n   ', (1912, 1923), self.input.position)
            _G_apply_124, lastError = self._apply(self.rule_other_hand, "other_hand", [])
            self.considerError(lastError, 'X_other_hand_X')
            _locals['m'] = _G_apply_124
            def _G_consumedby_125():
                def _G_many_126():
                    self._trace('marked_token*>', (1927, 1941), self.input.position)
                    _G_apply_127, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                    self.considerError(lastError, None)
                    return (_G_apply_127, self.currentError)
                _G_many_128, lastError = self.many(_G_many_126)
                self.considerError(lastError, None)
                return (_G_many_128, self.currentError)
            _G_consumedby_129, lastError = self.consumedby(_G_consumedby_125)
            self.considerError(lastError, 'X_other_hand_X')
            _locals['a2'] = _G_consumedby_129
            _G_python_131, lastError = eval(self._G_expr_130, self.globals, _locals), None
            self.considerError(lastError, 'X_other_hand_X')
            return (_G_python_131, self.currentError)


        def rule_part(self):
            _locals = {'self': self}
            self.locals['part'] = _locals
            _G_apply_132, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'part')
            _locals['what'] = _G_apply_132
            self._trace('e Parts\n# ################\n\npar', (2072, 2103), self.input.position)
            _G_apply_133, lastError = self._apply(self.rule_unmarked_lookahead_tokens, "unmarked_lookahead_tokens", [])
            self.considerError(lastError, 'part')
            _locals['search_in'] = _G_apply_133
            def _G_pred_134():
                _G_python_136, lastError = eval(self._G_expr_135, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_136, self.currentError)
            _G_pred_137, lastError = self.pred(_G_pred_134)
            self.considerError(lastError, 'part')
            _locals['p'] = _G_pred_137
            def _G_pred_138():
                _G_python_140, lastError = eval(self._G_expr_139, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_140, self.currentError)
            _G_pred_141, lastError = self.pred(_G_pred_138)
            self.considerError(lastError, 'part')
            _locals['l'] = _G_pred_141
            self._trace('factor=1)):p', (2223, 2235), self.input.position)
            _G_python_142, lastError = eval(self._G_expr_68, self.globals, _locals), None
            self.considerError(lastError, 'part')
            _G_apply_143, lastError = self._apply(self.rule_take, "take", [_G_python_142])
            self.considerError(lastError, 'part')
            _G_python_145, lastError = eval(self._G_expr_144, self.globals, _locals), None
            self.considerError(lastError, 'part')
            return (_G_python_145, self.currentError)


        def rule_subject(self):
            _locals = {'self': self}
            self.locals['subject'] = _locals
            self._trace('                \n    ', (2275, 2296), self.input.position)
            _G_python_146, lastError = ('subject'), None
            self.considerError(lastError, 'subject')
            _G_apply_147, lastError = self._apply(self.rule_part, "part", [_G_python_146])
            self.considerError(lastError, 'subject')
            _locals['s'] = _G_apply_147
            _G_python_149, lastError = eval(self._G_expr_148, self.globals, _locals), None
            self.considerError(lastError, 'subject')
            return (_G_python_149, self.currentError)


        def rule_aspect(self):
            _locals = {'self': self}
            self.locals['aspect'] = _locals
            self._trace("'subject'):s\n       ", (2326, 2346), self.input.position)
            _G_python_150, lastError = ('aspect'), None
            self.considerError(lastError, 'aspect')
            _G_apply_151, lastError = self._apply(self.rule_part, "part", [_G_python_150])
            self.considerError(lastError, 'aspect')
            _locals['s'] = _G_apply_151
            _G_python_152, lastError = eval(self._G_expr_148, self.globals, _locals), None
            self.considerError(lastError, 'aspect')
            return (_G_python_152, self.currentError)


        def rule_contrast(self):
            _locals = {'self': self}
            self.locals['contrast'] = _locals
            self._trace("part('aspect'):s\n     ", (2372, 2394), self.input.position)
            _G_python_153, lastError = ('contrast'), None
            self.considerError(lastError, 'contrast')
            _G_apply_154, lastError = self._apply(self.rule_part, "part", [_G_python_153])
            self.considerError(lastError, 'contrast')
            _locals['s'] = _G_apply_154
            _G_python_155, lastError = eval(self._G_expr_148, self.globals, _locals), None
            self.considerError(lastError, 'contrast')
            return (_G_python_155, self.currentError)


        def rule_difference_in(self):
            _locals = {'self': self}
            self.locals['difference_in'] = _locals
            _G_apply_156, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'difference_in')
            _locals['search_in'] = _G_apply_156
            def _G_pred_157():
                _G_python_159, lastError = eval(self._G_expr_158, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_159, self.currentError)
            _G_pred_160, lastError = self.pred(_G_pred_157)
            self.considerError(lastError, 'difference_in')
            _locals['contrasts'] = _G_pred_160
            def _G_pred_161():
                _G_python_163, lastError = eval(self._G_expr_162, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_163, self.currentError)
            _G_pred_164, lastError = self.pred(_G_pred_161)
            self.considerError(lastError, 'difference_in')
            _locals['subjects'] = _G_pred_164
            def _G_pred_165():
                _G_python_167, lastError = eval(self._G_expr_166, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_167, self.currentError)
            _G_pred_168, lastError = self.pred(_G_pred_165)
            self.considerError(lastError, 'difference_in')
            _locals['aspects'] = _G_pred_168
            _G_python_170, lastError = eval(self._G_expr_169, self.globals, _locals), None
            self.considerError(lastError, 'difference_in')
            return (_G_python_170, self.currentError)


        def rule_other_hand(self):
            _locals = {'self': self}
            self.locals['other_hand'] = _locals
            self._trace('tive, equative, assesitive\n\nother_hand = \n ', (3088, 3131), self.input.position)
            _G_python_172, lastError = eval(self._G_expr_171, self.globals, _locals), None
            self.considerError(lastError, 'other_hand')
            _G_apply_173, lastError = self._apply(self.rule_marker, "marker", [_G_python_172])
            self.considerError(lastError, 'other_hand')
            _locals['x'] = _G_apply_173
            _G_python_175, lastError = eval(self._G_expr_174, self.globals, _locals), None
            self.considerError(lastError, 'other_hand')
            return (_G_python_175, self.currentError)


        def rule_than(self):
            _locals = {'self': self}
            self.locals['than'] = _locals
            self._trace("tation('on_the_other_hand', x)  \n    ", (3203, 3240), self.input.position)
            _G_python_177, lastError = eval(self._G_expr_176, self.globals, _locals), None
            self.considerError(lastError, 'than')
            _G_apply_178, lastError = self._apply(self.rule_marker, "marker", [_G_python_177])
            self.considerError(lastError, 'than')
            _locals['x'] = _G_apply_178
            _G_python_180, lastError = eval(self._G_expr_179, self.globals, _locals), None
            self.considerError(lastError, 'than')
            return (_G_python_180, self.currentError)


        def rule_except(self):
            _locals = {'self': self}
            self.locals['except'] = _locals
            self._trace(" myself.marker_annotation('than', x)  \n", (3301, 3340), self.input.position)
            _G_python_182, lastError = eval(self._G_expr_181, self.globals, _locals), None
            self.considerError(lastError, 'except')
            _G_apply_183, lastError = self._apply(self.rule_marker, "marker", [_G_python_182])
            self.considerError(lastError, 'except')
            _locals['x'] = _G_apply_183
            _G_python_185, lastError = eval(self._G_expr_184, self.globals, _locals), None
            self.considerError(lastError, 'except')
            return (_G_python_185, self.currentError)


        def rule_the_same(self):
            _locals = {'self': self}
            self.locals['the_same'] = _locals
            self._trace(" -> myself.marker_annotation('except', x)", (3406, 3447), self.input.position)
            _G_python_187, lastError = eval(self._G_expr_186, self.globals, _locals), None
            self.considerError(lastError, 'the_same')
            _G_apply_188, lastError = self._apply(self.rule_marker, "marker", [_G_python_187])
            self.considerError(lastError, 'the_same')
            _locals['x'] = _G_apply_188
            _G_python_190, lastError = eval(self._G_expr_189, self.globals, _locals), None
            self.considerError(lastError, 'the_same')
            return (_G_python_190, self.currentError)


        def rule_as(self):
            _locals = {'self': self}
            self.locals['as'] = _locals
            self._trace("      -> myself.marker_annotation('", (3508, 3543), self.input.position)
            _G_python_192, lastError = eval(self._G_expr_191, self.globals, _locals), None
            self.considerError(lastError, 'as')
            _G_apply_193, lastError = self._apply(self.rule_marker, "marker", [_G_python_192])
            self.considerError(lastError, 'as')
            _locals['x'] = _G_apply_193
            _G_python_195, lastError = eval(self._G_expr_194, self.globals, _locals), None
            self.considerError(lastError, 'as')
            return (_G_python_195, self.currentError)


        def rule_while(self):
            _locals = {'self': self}
            self.locals['while'] = _locals
            self._trace("\n        -> myself.marker_annotation('a", (3601, 3640), self.input.position)
            _G_python_197, lastError = eval(self._G_expr_196, self.globals, _locals), None
            self.considerError(lastError, 'while')
            _G_apply_198, lastError = self._apply(self.rule_marker, "marker", [_G_python_197])
            self.considerError(lastError, 'while')
            _locals['x'] = _G_apply_198
            _G_python_200, lastError = eval(self._G_expr_199, self.globals, _locals), None
            self.considerError(lastError, 'while')
            return (_G_python_200, self.currentError)


        def rule_marker(self):
            _locals = {'self': self}
            self.locals['marker'] = _locals
            _G_apply_201, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'marker')
            _locals['f'] = _G_apply_201
            def _G_lookahead_202():
                def _G_consumedby_203():
                    def _G_many1_204():
                        self._trace('lf.marke', (3710, 3718), self.input.position)
                        _G_apply_205, lastError = self._apply(self.rule_anything, "anything", [])
                        self.considerError(lastError, None)
                        return (_G_apply_205, self.currentError)
                    _G_many1_206, lastError = self.many(_G_many1_204, _G_many1_204())
                    self.considerError(lastError, None)
                    return (_G_many1_206, self.currentError)
                _G_consumedby_207, lastError = self.consumedby(_G_consumedby_203)
                self.considerError(lastError, None)
                _locals['x'] = _G_consumedby_207
                return (_G_consumedby_207, self.currentError)
            _G_lookahead_208, lastError = self.lookahead(_G_lookahead_202)
            self.considerError(lastError, 'marker')
            def _G_pred_209():
                _G_python_211, lastError = eval(self._G_expr_210, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_211, self.currentError)
            _G_pred_212, lastError = self.pred(_G_pred_209)
            self.considerError(lastError, 'marker')
            _locals['n'] = _G_pred_212
            self._trace("hile', x", (3733, 3741), self.input.position)
            _G_python_214, lastError = eval(self._G_expr_213, self.globals, _locals), None
            self.considerError(lastError, 'marker')
            _G_apply_215, lastError = self._apply(self.rule_take, "take", [_G_python_214])
            self.considerError(lastError, 'marker')
            _locals['y'] = _G_apply_215
            _G_python_217, lastError = eval(self._G_expr_216, self.globals, _locals), None
            self.considerError(lastError, 'marker')
            return (_G_python_217, self.currentError)


        def rule_unmarked_token(self):
            _locals = {'self': self}
            self.locals['unmarked_token'] = _locals
            self._trace('ction: unmarked is anything not special\nunmarked_tok', (3831, 3883), self.input.position)
            _G_python_219, lastError = eval(self._G_expr_218, self.globals, _locals), None
            self.considerError(lastError, 'unmarked_token')
            _G_apply_220, lastError = self._apply(self.rule_marker, "marker", [_G_python_219])
            self.considerError(lastError, 'unmarked_token')
            _locals['y'] = _G_apply_220
            _G_python_221, lastError = eval(self._G_expr_216, self.globals, _locals), None
            self.considerError(lastError, 'unmarked_token')
            return (_G_python_221, self.currentError)


        def rule_punct(self):
            _locals = {'self': self}
            self.locals['punct'] = _locals
            self._trace('y\n        -> y \n      \n# Basic Tokens\n#', (3940, 3979), self.input.position)
            _G_python_223, lastError = eval(self._G_expr_222, self.globals, _locals), None
            self.considerError(lastError, 'punct')
            _G_apply_224, lastError = self._apply(self.rule_marker, "marker", [_G_python_223])
            self.considerError(lastError, 'punct')
            _locals['x'] = _G_apply_224
            _G_python_225, lastError = eval(self._G_expr_13, self.globals, _locals), None
            self.considerError(lastError, 'punct')
            return (_G_python_225, self.currentError)


        def rule_pseudo_sentence(self):
            _locals = {'self': self}
            self.locals['pseudo_sentence'] = _locals
            self._trace('    marker(grammar_fu', (4013, 4034), self.input.position)
            _G_apply_226, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
            self.considerError(lastError, 'pseudo_sentence')
            _locals['x'] = _G_apply_226
            self._trace('tions.', (4036, 4042), self.input.position)
            _G_apply_227, lastError = self._apply(self.rule_punct, "punct", [])
            self.considerError(lastError, 'pseudo_sentence')
            _locals['p'] = _G_apply_227
            _G_python_229, lastError = eval(self._G_expr_228, self.globals, _locals), None
            self.considerError(lastError, 'pseudo_sentence')
            return (_G_python_229, self.currentError)


        def rule_unmarked_lookahead_tokens(self):
            _locals = {'self': self}
            self.locals['unmarked_lookahead_tokens'] = _locals
            _G_apply_230, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'unmarked_lookahead_tokens')
            _locals['i'] = _G_apply_230
            def _G_lookahead_231():
                def _G_consumedby_232():
                    def _G_many1_233():
                        self._trace('    unmarked_t', (4094, 4108), self.input.position)
                        _G_apply_234, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                        self.considerError(lastError, None)
                        return (_G_apply_234, self.currentError)
                    _G_many1_235, lastError = self.many(_G_many1_233, _G_many1_233())
                    self.considerError(lastError, None)
                    return (_G_many1_235, self.currentError)
                _G_consumedby_236, lastError = self.consumedby(_G_consumedby_232)
                self.considerError(lastError, None)
                _locals['a'] = _G_consumedby_236
                return (_G_consumedby_236, self.currentError)
            _G_lookahead_237, lastError = self.lookahead(_G_lookahead_231)
            self.considerError(lastError, 'unmarked_lookahead_tokens')
            _G_python_239, lastError = eval(self._G_expr_238, self.globals, _locals), None
            self.considerError(lastError, 'unmarked_lookahead_tokens')
            return (_G_python_239, self.currentError)


        def rule_lookahead_tokens_no(self):
            _locals = {'self': self}
            self.locals['lookahead_tokens_no'] = _locals
            _G_apply_240, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'lookahead_tokens_no')
            _locals['i'] = _G_apply_240
            def _G_lookahead_241():
                def _G_consumedby_242():
                    def _G_repeat_243():
                        self._trace('\n    ~~(<unmar', (4163, 4177), self.input.position)
                        _G_apply_244, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
                        self.considerError(lastError, None)
                        return (_G_apply_244, self.currentError)
                    _G_repeat_245, lastError = self.repeat(_locals["i"], _locals["i"], _G_repeat_243)
                    self.considerError(lastError, None)
                    return (_G_repeat_245, self.currentError)
                _G_consumedby_246, lastError = self.consumedby(_G_consumedby_242)
                self.considerError(lastError, None)
                _locals['a'] = _G_consumedby_246
                return (_G_consumedby_246, self.currentError)
            _G_lookahead_247, lastError = self.lookahead(_G_lookahead_241)
            self.considerError(lastError, 'lookahead_tokens_no')
            _G_python_248, lastError = eval(self._G_expr_238, self.globals, _locals), None
            self.considerError(lastError, 'lookahead_tokens_no')
            return (_G_python_248, self.currentError)


        def rule_invisible_tokens(self):
            _locals = {'self': self}
            self.locals['invisible_tokens'] = _locals
            def _G_lookahead_249():
                def _G_consumedby_250():
                    def _G_many1_251():
                        self._trace('i = \n    ', (4228, 4237), self.input.position)
                        _G_apply_252, lastError = self._apply(self.rule_non_punct, "non_punct", [])
                        self.considerError(lastError, None)
                        return (_G_apply_252, self.currentError)
                    _G_many1_253, lastError = self.many(_G_many1_251, _G_many1_251())
                    self.considerError(lastError, None)
                    return (_G_many1_253, self.currentError)
                _G_consumedby_254, lastError = self.consumedby(_G_consumedby_250)
                self.considerError(lastError, None)
                return (_G_consumedby_254, self.currentError)
            _G_lookahead_255, lastError = self.lookahead(_G_lookahead_249)
            self.considerError(lastError, 'invisible_tokens')
            _locals['x'] = _G_lookahead_255
            _G_python_256, lastError = eval(self._G_expr_13, self.globals, _locals), None
            self.considerError(lastError, 'invisible_tokens')
            return (_G_python_256, self.currentError)


        def rule_take(self):
            _locals = {'self': self}
            self.locals['take'] = _locals
            _G_apply_257, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'take')
            _locals['i'] = _G_apply_257
            def _G_consumedby_258():
                def _G_repeat_259():
                    self._trace(' a\n\ninvi', (4274, 4282), self.input.position)
                    _G_apply_260, lastError = self._apply(self.rule_anything, "anything", [])
                    self.considerError(lastError, None)
                    return (_G_apply_260, self.currentError)
                _G_repeat_261, lastError = self.repeat(_locals["i"], _locals["i"], _G_repeat_259)
                self.considerError(lastError, None)
                return (_G_repeat_261, self.currentError)
            _G_consumedby_262, lastError = self.consumedby(_G_consumedby_258)
            self.considerError(lastError, 'take')
            _locals['x'] = _G_consumedby_262
            _G_python_263, lastError = eval(self._G_expr_13, self.globals, _locals), None
            self.considerError(lastError, 'take')
            return (_G_python_263, self.currentError)


        def rule_take_all(self):
            _locals = {'self': self}
            self.locals['take_all'] = _locals
            def _G_consumedby_264():
                def _G_many_265():
                    self._trace(':x\n      ', (4318, 4327), self.input.position)
                    _G_apply_266, lastError = self._apply(self.rule_non_punct, "non_punct", [])
                    self.considerError(lastError, None)
                    return (_G_apply_266, self.currentError)
                _G_many_267, lastError = self.many(_G_many_265)
                self.considerError(lastError, None)
                return (_G_many_267, self.currentError)
            _G_consumedby_268, lastError = self.consumedby(_G_consumedby_264)
            self.considerError(lastError, 'take_all')
            _locals['x'] = _G_consumedby_268
            _G_python_269, lastError = eval(self._G_expr_13, self.globals, _locals), None
            self.considerError(lastError, 'take_all')
            return (_G_python_269, self.currentError)


        def rule_non_punct(self):
            _locals = {'self': self}
            self.locals['non_punct'] = _locals
            self._trace('thing{i}>:x \n ', (4355, 4369), self.input.position)
            _G_apply_270, lastError = self._apply(self.rule_anything, "anything", [])
            self.considerError(lastError, 'non_punct')
            _locals['x'] = _G_apply_270
            def _G_pred_271():
                _G_python_273, lastError = eval(self._G_expr_272, self.globals, _locals), None
                self.considerError(lastError, None)
                return (_G_python_273, self.currentError)
            _G_pred_274, lastError = self.pred(_G_pred_271)
            self.considerError(lastError, 'non_punct')
            _G_python_275, lastError = eval(self._G_expr_13, self.globals, _locals), None
            self.considerError(lastError, 'non_punct')
            return (_G_python_275, self.currentError)


        def rule_word(self):
            _locals = {'self': self}
            self.locals['word'] = _locals
            self._trace('punct = \n    anything', (4430, 4451), self.input.position)
            _G_apply_276, lastError = self._apply(self.rule_unmarked_token, "unmarked_token", [])
            self.considerError(lastError, 'word')
            _locals['x'] = _G_apply_276
            _G_python_277, lastError = eval(self._G_expr_13, self.globals, _locals), None
            self.considerError(lastError, 'word')
            return (_G_python_277, self.currentError)


        _G_expr_4 = compile('d', '<string>', 'eval')
        _G_expr_13 = compile('x', '<string>', 'eval')
        _G_expr_19 = compile("search_in['difference']", '<string>', 'eval')
        _G_expr_23 = compile("{'difference': d,                           \n            'expansion':  search_in['expansion']}", '<string>', 'eval')
        _G_expr_29 = compile('myself.tokens_expansions(yet_parsed)', '<string>', 'eval')
        _G_expr_33 = compile('myself.tokens_expansions([[x, [None]]])', '<string>', 'eval')
        _G_expr_63 = compile('a1+a2, x', '<string>', 'eval')
        _G_expr_66 = compile('grammar_functions.subordinate_clause(m)', '<string>', 'eval')
        _G_expr_68 = compile('l', '<string>', 'eval')
        _G_expr_71 = compile('search_in', '<string>', 'eval')
        _G_expr_74 = compile("{'difference': d,\n             'expansion': [m]}", '<string>', 'eval')
        _G_expr_88 = compile("a1+a2, {'difference': [x],\n                   'expansion': [m]}", '<string>', 'eval')
        _G_expr_104 = compile("a1+a2, {'difference': [a,s],\n                   'expansion': [m]}", '<string>', 'eval')
        _G_expr_130 = compile("a1+a2, {'difference': None,\n            'expansion': [m]}", '<string>', 'eval')
        _G_expr_135 = compile('myself.delimit_by_match(search_in=search_in,  what=what, basic_factor=1)', '<string>', 'eval')
        _G_expr_139 = compile('myself.best_len(p)', '<string>', 'eval')
        _G_expr_144 = compile('p', '<string>', 'eval')
        _G_expr_148 = compile('s', '<string>', 'eval')
        _G_expr_158 = compile("myself.delimit_by_match(search_in=search_in, what='contrast', basic_factor=1, cant_fail=True, side_constraint='get all')", '<string>', 'eval')
        _G_expr_162 = compile("myself.delimit_by_match(search_in=search_in, what='subject', basic_factor=3,  cant_fail=True, side_constraint='get all')", '<string>', 'eval')
        _G_expr_166 = compile("myself.delimit_by_match(search_in=search_in, what='aspect', basic_factor=0, cant_fail=True, side_constraint='get all', min_sol=True)", '<string>', 'eval')
        _G_expr_169 = compile('[subjects, contrasts, aspects]', '<string>', 'eval')
        _G_expr_171 = compile('grammar_functions.other_hand_', '<string>', 'eval')
        _G_expr_174 = compile("myself.marker_annotation('on_the_other_hand', x)", '<string>', 'eval')
        _G_expr_176 = compile('grammar_functions.than_', '<string>', 'eval')
        _G_expr_179 = compile("myself.marker_annotation('than', x)", '<string>', 'eval')
        _G_expr_181 = compile('grammar_functions.except_', '<string>', 'eval')
        _G_expr_184 = compile("myself.marker_annotation('except', x)", '<string>', 'eval')
        _G_expr_186 = compile('grammar_functions.the_same_', '<string>', 'eval')
        _G_expr_189 = compile("myself.marker_annotation('the_same', x)", '<string>', 'eval')
        _G_expr_191 = compile('grammar_functions.as_', '<string>', 'eval')
        _G_expr_194 = compile("myself.marker_annotation('as', x)", '<string>', 'eval')
        _G_expr_196 = compile('grammar_functions.while_', '<string>', 'eval')
        _G_expr_199 = compile("myself.marker_annotation('while', x)", '<string>', 'eval')
        _G_expr_210 = compile('f(x)', '<string>', 'eval')
        _G_expr_213 = compile('n', '<string>', 'eval')
        _G_expr_216 = compile('y', '<string>', 'eval')
        _G_expr_218 = compile('grammar_functions.not_anything_special', '<string>', 'eval')
        _G_expr_222 = compile('grammar_functions.punct_', '<string>', 'eval')
        _G_expr_228 = compile('x, p', '<string>', 'eval')
        _G_expr_238 = compile('a', '<string>', 'eval')
        _G_expr_272 = compile('not grammar_functions.punct_([x])', '<string>', 'eval')
    if Grammar.globals is not None:
        Grammar.globals = Grammar.globals.copy()
        Grammar.globals.update(ruleGlobals)
    else:
        Grammar.globals = ruleGlobals
    return Grammar