import matplotlib.pyplot as plt
import numpy as np

labels = ['Программирование', 'Графы', 'Алгоритмы', 'Excel']
path = 'tmp.png'

def save_plot(val):
  global labels
  num_vars = len(labels)
  angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
  lab = labels + labels[:1]
  angles += angles[:1]

  fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

  def add_to_radar(car_model, color):
    values = val
    values += values[:1]
    ax.plot(angles, values, color=color, linewidth=1, label=car_model)
    ax.fill(angles, values, color=color, alpha=0.5)

  add_to_radar('rating user', '#1aaf6c')

  ax.set_theta_offset(np.pi / 2)
  ax.set_theta_direction(-1)

  ax.set_thetagrids(np.degrees(angles), lab)

  for label, angle in zip(ax.get_xticklabels(), angles):
    if angle in (0, np.pi):
      label.set_horizontalalignment('center')
    elif 0 < angle < np.pi:
      label.set_horizontalalignment('left')
    else:
      label.set_horizontalalignment('right')
  lim_y = min(max(val),90)
  ax.set_ylim(0, lim_y - (lim_y % -10))
  ax.set_rlabel_position(180 / num_vars)

  #ax.tick_params(colors='#222222')
  #ax.tick_params(axis='y', labelsize=8)
  #ax.grid(color='#AAAAAA')
  #ax.spines['polar'].set_color('#222222')
  #ax.set_facecolor('#FAFAFA')

  ax.set_title('RATING INFO EGE 2020', y=1.08)
  plt.savefig(path)
  return './' + path
