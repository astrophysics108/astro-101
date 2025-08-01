from manim import *


class CreateSquare(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation

class MovingAngle(Scene):
    def construct(self):
        rotation_center = LEFT

        theta_tracker = ValueTracker(110)
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)
        line_ref = line_moving.copy()
        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        )
        a = Angle(line1, line_moving, radius=0.5, other_angle=False)
        tex = MathTex(r"\theta").move_to(
            Angle(
                line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.5)
        )

        self.add(line1, line_moving, a, tex)
        self.wait()

        line_moving.add_updater(
            lambda x: x.become(line_ref.copy()).rotate(
                theta_tracker.get_value() * DEGREES, about_point=rotation_center
            )
        )

        a.add_updater(
            lambda x: x.become(Angle(line1, line_moving, radius=0.5, other_angle=False))
        )
        tex.add_updater(
            lambda x: x.move_to(
                Angle(
                    line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
                ).point_from_proportion(0.5)
            )
        )

        self.play(theta_tracker.animate.set_value(40))
        self.play(theta_tracker.animate.increment_value(140))
        self.play(tex.animate.set_color(RED), run_time=0.5)
        self.play(theta_tracker.animate.set_value(350))


from manim_physics import *

from manim import *
import numpy as np

class ElectricFieldManual(Scene):
    def construct(self):
        # Define charges: list of tuples (charge, position)
        charges = [
            (-1, np.array([-2, -1, 0])),
            (2, np.array([2, -1, 0])),
            (-1, np.array([0, 2, 0]))
        ]

        # Create dots for charges
        charge_dots = VGroup()
        for q, pos in charges:
            color = RED if q < 0 else BLUE
            dot = Dot(pos, color=color)
            charge_dots.add(dot)

        self.add(charge_dots)

        # Create a grid of points where to evaluate the field
        x_vals = np.linspace(-4, 4, 20)
        y_vals = np.linspace(-3, 3, 15)
        points = [np.array([x, y, 0]) for y in y_vals for x in x_vals]

        # Function to compute electric field vector at a point
        def electric_field_at_point(point):
            E = np.array([0.0, 0.0, 0.0])
            for q, pos in charges:
                r_vec = point - pos
                r_mag = np.linalg.norm(r_vec)
                if r_mag < 0.1:
                    continue  # Avoid division by zero near charge
                E += q * r_vec / r_mag**3
            return E

        # Create arrows for the field vectors
        arrows = VGroup()
        for p in points:
            E_vec = electric_field_at_point(p)
            E_mag = np.linalg.norm(E_vec)
            if E_mag == 0:
                continue
            # Normalize and scale arrow length
            direction = E_vec / E_mag
            arrow = Arrow(
                start=p,
                end=p + 0.3 * direction,
                buff=0,
                stroke_width=1,
                color=YELLOW
            )
            arrows.add(arrow)

        self.add(arrows)

        # Animation: move the third charge and update field arrows
        def update_arrows(mob):
            new_arrows = VGroup()
            # Update position of charge 3 dot
            charge_dots[2].move_to(charges[2][1])
            # Recalculate field at points
            for p in points:
                E = np.array([0.0, 0.0, 0.0])
                for i, (q, pos) in enumerate(charges):
                    r_vec = p - pos
                    r_mag = np.linalg.norm(r_vec)
                    if r_mag < 0.1:
                        continue
                    E += q * r_vec / r_mag**3
                E_mag = np.linalg.norm(E)
                if E_mag == 0:
                    continue
                direction = E / E_mag
                new_arrow = Arrow(
                    start=p,
                    end=p + 0.3 * direction,
                    buff=0,
                    stroke_width=1,
                    color=YELLOW
                )
                new_arrows.add(new_arrow)
            mob.become(new_arrows)

        arrows.add_updater(update_arrows)

        # Animate charge3 moving from initial pos to new pos
        new_pos = np.array([2, 2, 0])
        steps = 60
        for i in range(steps):
            alpha = (i + 1) / steps
            charges[2] = (charges[2][0], (1 - alpha) * charges[2][1] + alpha * new_pos)
            self.wait(0.05)

        arrows.remove_updater(update_arrows)
        self.wait(2)
