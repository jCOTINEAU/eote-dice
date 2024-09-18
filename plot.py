import matplotlib.pyplot as plt
import numpy as np
import operator
from dice import DicePool
from dice import Symbol

def update_annot(closest_x, closest_y,annot):
    annot.xy = (closest_x, closest_y)
    text = f"x = {closest_x}\nProbabilité: {closest_y}"
    annot.set_text(text)
    annot.get_bbox_patch().set_alpha(0.4)

# Event handling for mouse motion, using data from the line
def on_mouse_move(event, ax,fig, lines,annot):
    if event.inaxes == ax:  # Check if the mouse is inside the specific plot area (ax)
        closest_line = None
        min_dist = float('inf')  # Initialize with a large distance
        closest_x = None
        closest_y = None
        mouse_x = event.xdata
        mouse_y = event.ydata
        
        if mouse_x is not None and mouse_y is not None:
            # Round the mouse X to the nearest integer (since X values are integers)
            rounded_x = round(mouse_x)

            # Iterate through all lines to find the closest Y value
            for line in lines:
                x_data = line.get_xdata()  # Retrieve X data from the line
                y_data = line.get_ydata()  # Retrieve Y data from the line

                # Check if the rounded X exists in the current line's X data
                if rounded_x in x_data:
                    # Find the index of the rounded X in the X data of the line
                    idx = np.where(x_data == rounded_x)[0][0]
                    closest_y_line = y_data[idx]  # Get the Y value for this X in the current line

                    # Calculate the vertical distance (since X is already matched)
                    dist = abs(closest_y_line - mouse_y)

                    # Check if this line's point is the closest
                    if dist < min_dist:
                        min_dist = dist
                        closest_line = line
                        closest_x = rounded_x
                        closest_y = closest_y_line

            # If the closest Y distance is within the "sticky" range, update the annotation
            if min_dist < 0.25:  # Adjust this threshold if needed
                update_annot(closest_x, closest_y,annot)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                annot.set_visible(False)

class DicePlotter():
    def __init__(self):
        pass

    @staticmethod
    def plot(args):
        action = args.plotcommand

        if action == 'single':
            pool=args.pool
            symbols=args.Symbol
            upgrade=args.upgrade
            above=args.above

            for pool_string in pool:
                DicePlotter.plot_singles(symbols,upgrade,pool_string,above)
            plt.show()
        elif action == 'combined':
            pool=args.pool
            upgrade=args.upgrade
            compare=args.compare

            if compare:
                DicePlotter.plot_combined(upgrade,pool)
            else:
                for pool_string in pool:
                    DicePlotter.plot_combined(upgrade,[pool_string])
                
            plt.show()
        elif action == 'compare':
            pool=args.pool
            symbols=args.Symbol
            above=args.above

            DicePlotter.plot_compare(pool,symbols,above)
            plt.show()

    def plot_singles(symbols:dict[Symbol],upgrade: int=0,pool_string: str="",above=False):

        lines=[]
        dice_pool_function=DicePool.probability_above if above else DicePool.probability
        fig,ax = DicePlotter.init_plot()
        annot = ax.annotate("", xy=(0,0), xytext=(10,10),
                            textcoords="offset points", 
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))

        annot.set_visible(False)
        ax.set_title(DicePlotter.get_single_title(symbols,DicePool._bad_dice_to_string(pool_string)))
        ax.set_ylim(0,100)

        for symbol in symbols:
            cutoffs=[None,None,None,None]
            if symbol == Symbol.Triumph:
                label='Triumph'
                cutoffs[0] = 1
            elif symbol == Symbol.Success:
                label='Success'
                cutoffs[1] = 1
            elif symbol == Symbol.Advantage:
                label='Advantage'
                cutoffs[2] = 1
            elif symbol == Symbol.Despair:
                label='Despair'
                cutoffs[3] = 1


            for i in range(0,upgrade+1):
                x_axis_value = []
                y_axis_value = []
                upgraded_pool=DicePool._upgrade_dice_pool_string_with_proficency(pool_string=pool_string,upgrade=i)
                dice_pool = DicePool.from_string(upgraded_pool)
                median = dice_pool.median()
                mean=dice_pool.mean_tuple()
                std=dice_pool.standard_deviation()
                for i in range(-4,5):
                    x_axis_value.append(i)
                    y_axis_value.append(round(dice_pool_function(self=dice_pool,
                        triumph_cutoff=cutoffs[0]*i if cutoffs and cutoffs[0] is not None else None,
                        success_cutoff=cutoffs[1]*i if cutoffs and cutoffs[1] is not None else None,
                        advantage_cutoff=cutoffs[2]*i if cutoffs and cutoffs[2] is not None else None,
                        despair_cutoff=cutoffs[3]*i if cutoffs and cutoffs[3] is not None else None
                        )
                    * 100))
                line,=ax.plot(x_axis_value, y_axis_value,label="{}: {}, median: {}, mean: {}, std: {}".format(label,DicePool._good_dice_to_string(upgraded_pool),
                    (median[0] if cutoffs and cutoffs[0] is not None else 0)+(median[1] if cutoffs and cutoffs[1] is not None else 0)+(median[2] if cutoffs and cutoffs[2] is not None else 0)+(median[3] if cutoffs and cutoffs[3] is not None else 0),
                    round((mean[0] if cutoffs and cutoffs[0] is not None else 0)+(mean[1] if cutoffs and cutoffs[1] is not None else 0)+(mean[2] if cutoffs and cutoffs[2] is not None else 0)+(mean[3] if cutoffs and cutoffs[3] is not None else 0),2),
                    round((std[0] if cutoffs and cutoffs[0] is not None else 0)+(std[1] if cutoffs and cutoffs[1] is not None else 0)+(std[2] if cutoffs and cutoffs[2] is not None else 0)+(std[3] if cutoffs and cutoffs[3] is not None else 0),2)
                    ))
                lines.append(line)

        fig.canvas.mpl_connect("motion_notify_event", lambda event: on_mouse_move(event, ax,fig,lines,annot))

        ax.legend()
    
    def plot_combined(upgrade: int=0,pool: list[str]=[]):
        
        fig,ax = DicePlotter.init_plot()
        title=""
        for pool_string in pool:
            title+="-"+DicePool._bad_dice_to_string(pool_string)
        ax.set_title(DicePlotter.get_combined_title(title))
        ax.set_ylim(0,100)
        annot = ax.annotate("", xy=(0,0), xytext=(10,10),
                            textcoords="offset points", 
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))

        annot.set_visible(False)
        lines=[]
        
        for pool_string in pool:

            for i in range(0,upgrade+1):
                x_axis_value = []
                y_axis_value = []
                upgraded_pool=DicePool._upgrade_dice_pool_string_with_proficency(pool_string=pool_string,upgrade=i)
                dice_pool = DicePool.from_string(upgraded_pool)

                x_axis_value.append(0)
                y_axis_value.append(round(dice_pool.probability_with_operator(triumph_cutoff=None,success_cutoff=[0,operator.le],advantage_cutoff=[0,operator.le],despair_cutoff=None)*100))
                x_axis_value.append(1)
                y_axis_value.append(round(dice_pool.probability_with_operator(triumph_cutoff=None,success_cutoff=[0,operator.le],advantage_cutoff=[1,operator.ge],despair_cutoff=None)*100))
                x_axis_value.append(2)
                y_axis_value.append(round(dice_pool.probability_with_operator(triumph_cutoff=None,success_cutoff=[1,operator.ge],advantage_cutoff=[0,operator.le],despair_cutoff=None)*100))
                x_axis_value.append(3)
                y_axis_value.append(round(dice_pool.probability_with_operator(triumph_cutoff=None,success_cutoff=[1,operator.ge],advantage_cutoff=[1,operator.ge],despair_cutoff=None)*100))
                x_axis_value.append(4)
                y_axis_value.append(round(dice_pool.probability_with_operator(triumph_cutoff=None,success_cutoff=[1,operator.ge],advantage_cutoff=[3,operator.ge],despair_cutoff=None)*100))
                x_axis_value.append(5)
                y_axis_value.append(round(dice_pool.probability_with_operator(triumph_cutoff=[1,operator.ge],success_cutoff=[1,operator.ge],advantage_cutoff=None,despair_cutoff=None)*100))
                line,=ax.plot(x_axis_value, y_axis_value,label="{}".format(DicePool._good_dice_to_string(upgraded_pool)))
                lines.append(line)

                ax.set_xticks([0,1,2,3,4,5])
                ax.set_xticklabels(["-s/-a","-s/+a","+s/-a","+s/+a","+s/+3a","s+/T+"])
                fig.canvas.mpl_connect("motion_notify_event", lambda event: on_mouse_move(event, ax,fig,lines,annot))

        ax.legend()

    def plot_compare(pool: list[str],symbols:dict[Symbol],above=False):

        dice_pool_function=DicePool.probability_above if above else DicePool.probability
        lines=[]
        fig,ax = DicePlotter.init_plot()
        ax.set_title("Comparison of dice pools")
        annot = ax.annotate("", xy=(0,0), xytext=(10,10),
                            textcoords="offset points", 
                            bbox=dict(boxstyle="round", fc="w"),
                            arrowprops=dict(arrowstyle="->"))

        annot.set_visible(False)
        ax.set_ylim(0,100)
        
        for symbol in symbols:
            cutoffs=[None,None,None,None]
            if symbol == Symbol.Triumph:
                label='Triumph'
                cutoffs[0] = 1
            elif symbol == Symbol.Success:
                label='Success'
                cutoffs[1] = 1
            elif symbol == Symbol.Advantage:
                label='Advantage'
                cutoffs[2] = 1
            elif symbol == Symbol.Despair:
                label='Despair'
                cutoffs[3] = 1

            for pool_string in pool:
                x_axis_value = []
                y_axis_value = []
                dice_pool = DicePool.from_string(pool_string)
                median = dice_pool.median()
                mean=dice_pool.mean_tuple()
                std=dice_pool.standard_deviation()
                for i in range(-4,5):
                    x_axis_value.append(i)
                    y_axis_value.append(round(dice_pool_function(self=dice_pool,
                        triumph_cutoff=cutoffs[0]*i if cutoffs and cutoffs[0] is not None else None,
                        success_cutoff=cutoffs[1]*i if cutoffs and cutoffs[1] is not None else None,
                        advantage_cutoff=cutoffs[2]*i if cutoffs and cutoffs[2] is not None else None,
                        despair_cutoff=cutoffs[3]*i if cutoffs and cutoffs[3] is not None else None
                        )
                    * 100))
                line,=ax.plot(x_axis_value, y_axis_value,label="{}: {}, median: {}, mean: {}, std: {}".format(label,pool_string,
                    (median[0] if cutoffs and cutoffs[0] is not None else 0)+(median[1] if cutoffs and cutoffs[1] is not None else 0)+(median[2] if cutoffs and cutoffs[2] is not None else 0)+(median[3] if cutoffs and cutoffs[3] is not None else 0),
                    round((mean[0] if cutoffs and cutoffs[0] is not None else 0)+(mean[1] if cutoffs and cutoffs[1] is not None else 0)+(mean[2] if cutoffs and cutoffs[2] is not None else 0)+(mean[3] if cutoffs and cutoffs[3] is not None else 0),2),
                    round((std[0] if cutoffs and cutoffs[0] is not None else 0)+(std[1] if cutoffs and cutoffs[1] is not None else 0)+(std[2] if cutoffs and cutoffs[2] is not None else 0)+(std[3] if cutoffs and cutoffs[3] is not None else 0),2)
                    ))
                lines.append(line)

        fig.canvas.mpl_connect("motion_notify_event", lambda event: on_mouse_move(event, ax,fig,lines,annot))

        ax.legend()


    def get_single_title(symbols:dict[Symbol],pool_string: str="") -> str:
        terms = []
        
        if Symbol.Triumph in symbols:
            terms.append('Triumph')
        if Symbol.Success in symbols:
            terms.append('Success')
        if Symbol.Advantage in symbols:
            terms.append('Advantage')
        if Symbol.Despair in symbols:
            terms.append('Despair')
        
        return f"{"Experimental" if DicePool.is_experimental else "Standard" }: Distribution of {', '.join(terms)} on {pool_string} dice pool."

    def get_combined_title(pool_string: str="") -> str:
        terms = []
        
        return f"{"Experimental" if DicePool.is_experimental else "Standard" }: Distribution on {pool_string} dice pool."
    def init_plot() -> plt.Figure and plt.Axes:
        fig,ax = plt.subplots()
        return fig,ax
