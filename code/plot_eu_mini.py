import csv
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SUMMARY_FILE = ROOT_DIR / "code" / "outputs" / "eu_mini_case_summary.csv"
OUTPUT_FILE = ROOT_DIR / "code" / "outputs" / "eu_mini_population_vs_banzhaf.svg"


def load_summary(path):
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    for row in rows:
        row["Population Share"] = float(row["Population Share"])
        row["Normalized Banzhaf Index"] = float(row["Normalized Banzhaf Index"])
        row["Population (millions)"] = float(row["Population (millions)"])
        row["Critical Count"] = int(row["Critical Count"])

    return rows


def scale_x(value, left, width):
    return left + value * width


def scale_y(value, top, height):
    return top + height - value * height


def build_svg(rows):
    width = 980
    height = 640
    margin_left = 110
    margin_right = 70
    margin_top = 90
    margin_bottom = 100

    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    x_ticks = [0.0, 0.1, 0.2, 0.3, 0.4]
    y_ticks = [0.0, 0.1, 0.2, 0.3, 0.4]

    palette = ["#1f4e79", "#c84c09", "#2a7f62", "#8b1e3f", "#7a6c00", "#5b4ea3"]

    svg = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
    )
    svg.append("<title id=\"title\">Population Share vs Banzhaf Power</title>")
    svg.append(
        "<desc id=\"desc\">Scatter plot for the six-country EU dual-majority mini-model. "
        "The x-axis shows population share and the y-axis shows normalized Banzhaf index.</desc>"
    )
    svg.append(
        '<rect x="0" y="0" width="100%" height="100%" fill="#f8f6f1"/>'
    )
    svg.append(
        f'<text x="{margin_left}" y="44" font-family="Georgia, serif" font-size="28" '
        'font-weight="700" fill="#1f2933">Population Share vs. Banzhaf Power</text>'
    )
    svg.append(
        f'<text x="{margin_left}" y="70" font-family="Georgia, serif" font-size="15" '
        'fill="#3f4c5a">EU dual-majority mini-model with 6 countries, 4-state threshold, and 65% population threshold</text>'
    )

    plot_x = margin_left
    plot_y = margin_top

    svg.append(
        f'<rect x="{plot_x}" y="{plot_y}" width="{plot_width}" height="{plot_height}" '
        'fill="#fffdf8" stroke="#d6d0c4" stroke-width="1.5"/>'
    )

    for tick in x_ticks:
        x = scale_x(tick / 0.4, plot_x, plot_width)
        svg.append(
            f'<line x1="{x:.2f}" y1="{plot_y}" x2="{x:.2f}" y2="{plot_y + plot_height}" '
            'stroke="#e5ded1" stroke-width="1"/>'
        )
        svg.append(
            f'<text x="{x:.2f}" y="{plot_y + plot_height + 28}" text-anchor="middle" '
            'font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#4f5b67">'
            f"{tick:.0%}</text>"
        )

    for tick in y_ticks:
        y = scale_y(tick / 0.4, plot_y, plot_height)
        svg.append(
            f'<line x1="{plot_x}" y1="{y:.2f}" x2="{plot_x + plot_width}" y2="{y:.2f}" '
            'stroke="#e5ded1" stroke-width="1"/>'
        )
        svg.append(
            f'<text x="{plot_x - 16}" y="{y + 4:.2f}" text-anchor="end" '
            'font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#4f5b67">'
            f"{tick:.0%}</text>"
        )

    x_axis_y = plot_y + plot_height
    y_axis_x = plot_x
    svg.append(
        f'<line x1="{plot_x}" y1="{x_axis_y}" x2="{plot_x + plot_width}" y2="{x_axis_y}" '
        'stroke="#53616f" stroke-width="2"/>'
    )
    svg.append(
        f'<line x1="{y_axis_x}" y1="{plot_y}" x2="{y_axis_x}" y2="{plot_y + plot_height}" '
        'stroke="#53616f" stroke-width="2"/>'
    )

    equality_points = []
    for tick in [i / 100 for i in range(0, 41)]:
        x = scale_x(tick / 0.4, plot_x, plot_width)
        y = scale_y(tick / 0.4, plot_y, plot_height)
        equality_points.append(f"{x:.2f},{y:.2f}")
    svg.append(
        f'<polyline points="{" ".join(equality_points)}" fill="none" '
        'stroke="#b3a58a" stroke-width="2" stroke-dasharray="8 6"/>'
    )
    svg.append(
        f'<text x="{plot_x + plot_width - 10}" y="{plot_y + 18}" text-anchor="end" '
        'font-family="Helvetica, Arial, sans-serif" font-size="12" fill="#7b6f5b">equal power and population share</text>'
    )

    for index, row in enumerate(rows):
        x_ratio = min(row["Population Share"] / 0.4, 1.0)
        y_ratio = min(row["Normalized Banzhaf Index"] / 0.4, 1.0)
        x = scale_x(x_ratio, plot_x, plot_width)
        y = scale_y(y_ratio, plot_y, plot_height)
        color = palette[index % len(palette)]

        svg.append(
            f'<line x1="{x:.2f}" y1="{x_axis_y}" x2="{x:.2f}" y2="{y:.2f}" '
            f'stroke="{color}" stroke-width="2" stroke-opacity="0.4"/>'
        )
        svg.append(
            f'<circle cx="{x:.2f}" cy="{y:.2f}" r="7.5" fill="{color}" stroke="#fffdf8" stroke-width="2"/>'
        )

        label_dx = 12 if row["Country"] not in {"Germany", "France"} else -12
        anchor = "start" if label_dx > 0 else "end"
        label_dy = -12 if row["Country"] in {"Netherlands", "Luxembourg", "Malta"} else -10

        svg.append(
            f'<text x="{x + label_dx:.2f}" y="{y + label_dy:.2f}" text-anchor="{anchor}" '
            'font-family="Helvetica, Arial, sans-serif" font-size="13" font-weight="700" '
            f'fill="{color}">{row["Country"]}</text>'
        )
    svg.append(
        f'<text x="{plot_x + plot_width / 2:.2f}" y="{height - 28}" text-anchor="middle" '
        'font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#1f2933">Population Share</text>'
    )
    svg.append(
        f'<text x="28" y="{plot_y + plot_height / 2:.2f}" text-anchor="middle" '
        'font-family="Helvetica, Arial, sans-serif" font-size="15" fill="#1f2933" '
        f'transform="rotate(-90 28 {plot_y + plot_height / 2:.2f})">Normalized Banzhaf Index</text>'
    )
    svg.append(
        f'<text x="{plot_x}" y="{height - 8}" font-family="Helvetica, Arial, sans-serif" '
        'font-size="12" fill="#5f6b76">Generated from code/outputs/eu_mini_case_summary.csv</text>'
    )
    svg.append("</svg>")

    return "\n".join(svg) + "\n"


def main():
    rows = load_summary(SUMMARY_FILE)
    svg = build_svg(rows)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(svg, encoding="utf-8")
    print(f"Saved plot to {OUTPUT_FILE.relative_to(ROOT_DIR)}")


if __name__ == "__main__":
    main()
