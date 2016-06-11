from progressbar import ProgressBar, Bar, Percentage, AdaptiveETA, Counter, Timer


def get_progress_bar(n):
  # progress bar
  pbar_widgets = ['IMU Epochs : ', Bar(marker='#'), 'epoch=', Counter(), ' ', Percentage(), ' (', Timer(), ') ', AdaptiveETA(), ' ']
  pbar = ProgressBar(widgets=pbar_widgets, maxval=n).start()
  return pbar
