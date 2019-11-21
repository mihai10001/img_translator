from spellchecker import SpellChecker
from string_ops import word_split, word_join

# Languages supported by pyspellchecker by default
# Based on frequency list dictionaries, you can easily add more
supported_langs = ['en', 'es', 'de', 'fr', 'pt']


# advanced = False
def spell_check_v2(string, language):
    if language in supported_langs:
        spell = SpellChecker(language=language)
        words = word_split(string)
        misspelled = spell.unknown(words)

        words = [spell.correction(word) if word in misspelled else word for word in words]
        return word_join(words)


repeat = 20
# timers
import timeit
import numpy as np
v1_returns = timeit.repeat("spell_check_v1('whoze houze is dis?', 'en')", "from __main__ import spell_check_v1", number=10, repeat=repeat)
v2_returns = timeit.repeat("spell_check_v2('whoze houze is dis?', 'en')", "from __main__ import spell_check_v2", number=10, repeat=repeat)
v1_returns = np.array(v1_returns)
v2_returns = np.array(v2_returns)

# plot
import matplotlib.pyplot as plt
time_range = range(0, repeat)

plt.plot(time_range, v1_returns, 'r', label='v1 Timings')
plt.plot(time_range, v2_returns, 'b', label='v2 Timings')
plt.fill_between(time_range, v1_returns, v2_returns, where=v2_returns <= v1_returns, facecolor='r', interpolate=True)
plt.fill_between(time_range, v1_returns, v2_returns, where=v2_returns >= v1_returns, facecolor='b', interpolate=True)
plt.title('Timing differences between v1 and v2 - filled')
plt.xlabel('Time')
plt.ylabel('Timing functions')
plt.legend()
plt.show()
