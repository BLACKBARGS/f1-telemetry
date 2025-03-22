import customtkinter as ctk
from data_handler import F1DataHandler
from plotter import F1Plotter
from ui import F1UI

def main():
    """Start do programa."""
    root = ctk.CTk()
    data_handler = F1DataHandler()
    plotter = F1Plotter(graph_frame=None)
    ui = F1UI(root, data_handler, plotter)
    plotter.graph_frame = ui.graph_frame
    root.mainloop()

if __name__ == "__main__":
    main()