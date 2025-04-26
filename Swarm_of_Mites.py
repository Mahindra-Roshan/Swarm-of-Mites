import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from IPython.display import HTML
class CodeMite:
    def __init__(self, dna, x, y):
        self.dna = dna
        self.x = x
        self.y = y
        self.energy = 15
    def act(self):
        points = []
        for action in self.dna:
            if action == "move":
                self.x += 1
            elif action == "left":
                self.x -= 1
            elif action == "up":
                self.y += 1
            elif action == "down":
                self.y -= 1
            elif action == "jump":
                self.x += random.randint(2, 5)
                self.y += random.randint(-2, 2)
            elif action == "spin":
                self.x += random.choice([-1, 0, 1])
                self.y += random.choice([-1, 0, 1])
            elif action == "purr":
                points.append((self.x, self.y))
                points.append((self.x + 1, self.y + 1))
            elif action == "draw":
                points.append((self.x, self.y))
            elif action == "split" and self.energy > 10:
                return "split", points
        self.energy -= 0.5  # Slower energy drain
        return None, points
# meme dna
meme_actions = {
    "dank_memes": ["jump", "spin", "draw"],
    "cat_videos": ["up", "purr", "split"],
    "vibe_check": ["left", "down", "move"]
}
# starting with one mite
initial_dna = meme_actions["dank_memes"] + ["up", "split"]
swarm = [CodeMite(initial_dna, 0, 0)]
def update_swarm():
    global swarm
    new_swarm = []
    points = []
    for mite in swarm:
        result, new_points = mite.act()
        points.extend(new_points)
        if result == "split" and random.random() < 0.1:  #10 percent split  chance here
            new_dna = mite.dna.copy()
            if random.random() < 0.5:
                new_dna.append(random.choice(list(meme_actions.values())[random.randint(0, 2)]))
            new_swarm.append(CodeMite(new_dna, mite.x, mite.y))
            points.append((mite.x, mite.y))
        if mite.energy > 0:
            new_swarm.append(mite)
    swarm = new_swarm
    return points

# progress animation setup
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_facecolor("black")
plt.title("Swarm of mites")
plt.xlabel("X Position")
plt.ylabel("Y Position")

scat = ax.scatter([], [], c="white", s=20)
ax.set_xlim(-20, 50)
ax.set_ylim(-20, 50)

# i limit the  points  to 500
all_points = []

def update(frame):
    points = update_swarm()
    all_points.extend(points)
    if len(all_points) > 500:  # 500 points
        all_points[:] = all_points[-500:]
    if all_points:
        x_vals, y_vals = zip(*all_points)
        scat.set_offsets(list(zip(x_vals, y_vals)))
        max_x = max(mite.x for mite in swarm) + 10 if swarm else 50
        min_x = min(mite.x for mite in swarm) - 10 if swarm else -20
        max_y = max(mite.y for mite in swarm) + 10 if swarm else 50
        min_y = min(mite.y for mite in swarm) - 10 if swarm else -20
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
    return scat,

#animation with fewer frames to test
ani = animation.FuncAnimation(fig, update, frames=150, interval=100, blit=True)

HTML(ani.to_jshtml())