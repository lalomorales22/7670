from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # List of visualizations
    visualizations = [
        {'name': 'Fractal Tree', 'id': 'fractal_tree'},
        {'name': 'Psychedelic Vortex', 'id': 'psychedelic_vortex'},
        {'name': 'Neon Waves', 'id': 'neon_waves'},
        {'name': 'Kaleidoscope', 'id': 'kaleidoscope'},
        {'name': 'Particle Explosion', 'id': 'particle_explosion'},
        {'name': 'Matrix Rain', 'id': 'matrix_rain'},
        {'name': 'Fireworks', 'id': 'fireworks'},
        {'name': 'Gravity Balls', 'id': 'gravity_balls'},
        {'name': 'Perlin Noise Flow Field', 'id': 'perlin_noise_flow_field'},
        {'name': 'Mandelbrot Set', 'id': 'mandelbrot_set'},
        {'name': 'Starfield', 'id': 'starfield'},
        {'name': '3D Rotating Cube', 'id': 'rotating_cube'},
        {'name': 'Circular Wave', 'id': 'circular_wave'},
        {'name': 'Spiral Galaxy', 'id': 'spiral_galaxy'},
        {'name': 'Lightning Effect', 'id': 'lightning_effect'},
        {'name': 'Colorful Spirograph', 'id': 'spirograph'},
        {'name': 'Audio Visualizer', 'id': 'audio_visualizer'},
        {'name': 'Hypnotic Squares', 'id': 'hypnotic_squares'},
        {'name': 'Metaballs', 'id': 'metaballs'}
    ]
    return render_template('index.html', visualizations=visualizations)

if __name__ == '__main__':
    app.run(debug=True)
