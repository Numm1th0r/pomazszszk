# -*- coding: utf-8 -*-
"""Egyszerű, vonalas SVG ikonkészlet (24x24, stroke alapú)."""

_PATHS = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.1a2 2 0 0 1 2.1-.5c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
    "pin": '<path d="M20 10c0 4.99-5.1 9.6-7.2 11.3a1.3 1.3 0 0 1-1.6 0C9.1 19.6 4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "arrow-right": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "close": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "soup": '<path d="M4 11h16a1 1 0 0 1 1 1 8 8 0 0 1-8 8h-2a8 8 0 0 1-8-8 1 1 0 0 1 1-1Z"/><path d="M8.5 8a1.8 1.8 0 0 0 0-2.5 1.8 1.8 0 0 1 0-2.5"/><path d="M12 8a1.8 1.8 0 0 0 0-2.5 1.8 1.8 0 0 1 0-2.5"/><path d="M15.5 8a1.8 1.8 0 0 0 0-2.5 1.8 1.8 0 0 1 0-2.5"/>',
    "home-heart": '<path d="m3 10 9-7 9 7v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/><path d="M12 17.5s-2.8-1.9-2.8-3.6a1.7 1.7 0 0 1 2.8-1.2 1.7 1.7 0 0 1 2.8 1.2c0 1.7-2.8 3.6-2.8 3.6Z"/>',
    "bell": '<path d="M6 8a6 6 0 1 1 12 0c0 5 2 6 2 6H4s2-1 2-6"/><path d="M10.3 20a2 2 0 0 0 3.4 0"/>',
    "users": '<path d="M16 20v-1.5a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4V20"/><circle cx="9" cy="7" r="3.5"/><path d="M22 20v-1.5a4 4 0 0 0-3-3.9"/><path d="M16.5 3.7a4 4 0 0 1 0 6.6"/>',
    "building": '<path d="M4 21V6a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v15"/><path d="M16 10h2a2 2 0 0 1 2 2v9"/><path d="M2 21h20"/><path d="M8 8h2"/><path d="M8 12h2"/><path d="M8 16h2"/>',
    "hand-heart": '<path d="M11 14h2a2 2 0 0 0 0-4H9.5L7 12"/><path d="m2 15 4 4 5-1 5.5-2.5a2 2 0 0 0-2-3.4"/><path d="M13.5 7.5s-2-1.3-2-2.7A1.5 1.5 0 0 1 14 3.8a1.5 1.5 0 0 1 2.5 1c0 1.4-2 2.7-2 2.7Z"/>',
    "stethoscope": '<path d="M4 3v6a4 4 0 0 0 8 0V3"/><path d="M4 3H2.5M12 3h1.5"/><path d="M8 13v2a5 5 0 0 0 10 0v-1"/><circle cx="18" cy="11" r="2.5"/>',
    "bus": '<path d="M4 17V6a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v11"/><path d="M4 11h16"/><path d="M2 17h20"/><circle cx="7.5" cy="19.5" r="1.5"/><circle cx="16.5" cy="19.5" r="1.5"/><path d="M8 7h8"/>',
    "file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5"/><path d="M9 13h6"/><path d="M9 17h4"/>',
    "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="1.6"/><path d="m21 16-5-5-6 6-2-2-5 5"/>',
    "info": '<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 7.6h.01"/>',
    "alert": '<path d="M10.3 3.9 1.9 18a2 2 0 0 0 1.7 3h16.8a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><path d="M2 12h20"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    "external": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><path d="M15 3h6v6"/><path d="M10 14 21 3"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M16 3v4M8 3v4M3 11h18"/>',
    "shield": '<path d="M12 22s8-4 8-10V5.5l-8-3-8 3V12c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
    "accessibility": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="7.5" r="1.2"/><path d="M8 10.2c2.6.8 5.4.8 8 0"/><path d="M12 10.5V15"/><path d="m9.6 18.4 1.6-3.4h1.6l1.6 3.4"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "scale": '<path d="M12 3v18"/><path d="M7 21h10"/><path d="m5 7 14-2"/><path d="M5 7 2.5 13a3 3 0 0 0 5 0Z"/><path d="m19 5 2.5 6a3 3 0 0 1-5 0Z"/>',
    "heart": '<path d="M20.8 5.6a5 5 0 0 0-7.1 0L12 7.3l-1.7-1.7a5 5 0 1 0-7.1 7.1l8.1 8.1a1 1 0 0 0 1.4 0l8.1-8.1a5 5 0 0 0 0-7.1Z"/>',
    "sparkle": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4"/><path d="M12 8.5 13.4 11 16 12l-2.6 1-1.4 2.5L10.6 13 8 12l2.6-1Z"/>',
    "book": '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5Z"/><path d="M4 17.5h16"/>',
    "chat": '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 21l1.9-5.4A8 8 0 1 1 21 12Z"/>',
}


def icon(name, cls="", size=None):
    body = _PATHS.get(name, _PATHS["info"])
    dims = f' width="{size}" height="{size}"' if size else ""
    c = f' class="{cls}"' if cls else ""
    return (
        f'<svg{c}{dims} viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
        f'aria-hidden="true" focusable="false">{body}</svg>'
    )


LOGO = (
    '<svg class="brand__mark" viewBox="0 0 48 48" role="img" aria-label="Szociális Szolgáltatási Központ Pomáz embléma">'
    '<rect width="48" height="48" rx="13" fill="#1d5b4f"/>'
    '<path d="M24 11.5 35.5 20v14.5a2 2 0 0 1-2 2h-19a2 2 0 0 1-2-2V20Z" fill="none" stroke="#f5efe3" stroke-width="2.4" stroke-linejoin="round"/>'
    '<path d="M24 31.4s-5.1-3.3-5.1-6.3a2.9 2.9 0 0 1 5.1-1.9 2.9 2.9 0 0 1 5.1 1.9c0 3-5.1 6.3-5.1 6.3Z" fill="#e08e5a"/>'
    '</svg>'
)
